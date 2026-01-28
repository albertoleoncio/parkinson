from django.core.management.base import BaseCommand

from data.models import Page, Pageviews
import requests
from datetime import datetime, timedelta

class Command(BaseCommand):

    def handle(self, *args, **options):
        # end_date wil be the last day of all edits in the Query model. For example, between all pages, if the last edit is 2023-08-15, end_date will be 2023081500.
        end_date = None
        for page in Page.objects.all():
            try:
                query = page.query
                revisions = query.json.get('query', {}).get('pages', [])[0].get('revisions', [])
                for rev in revisions:
                    rev_date = datetime.strptime(rev['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                    if end_date is None or rev_date > end_date:
                        end_date = rev_date
            except Query.DoesNotExist:
                continue
        print(f"End date for pageviews collection is {end_date.strftime('%Y-%m-%d')}")

        start_date = end_date - timedelta(days=365)
        start_str = start_date.strftime('%Y%m%d00')
        end_str = end_date.strftime('%Y%m%d00')

        for page in Page.objects.all():
            print(f"+ Processing page {page.language_code} - {page.page_name}")
            try:
                Pageviews.objects.get(page=page)
            except Pageviews.DoesNotExist:
                print(f"Pageviews for {page.page_name} not found. Loading pageviews.")
                lang = page.language_code.replace('_', '-')
                
                url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{lang}.wikipedia/all-access/user/{page.page_name}/daily/{start_str}/{end_str}"
                
                headers = {"User-Agent": "parkinson/1.0 (+https://github.com/albertoleoncio/parkinson)"}
                response = requests.get(url, headers=headers)
                data = response.json()
                
                total_views = sum(item['views'] for item in data.get('items', []))
                
                pageviews = Pageviews.objects.create(page=page, views=total_views)
                print(f"Pageviews for {page.page_name} created with id {pageviews.id} and total views {total_views}.")
