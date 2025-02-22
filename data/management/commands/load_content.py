from django.core.management.base import BaseCommand
from data.models import Page, Parser, Query
import requests

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for page in Page.objects.all():
            print(f"+ Processing page {page.language_code} - {page.page_name}")
            try:
                Parser.objects.get(page=page)
            except Parser.DoesNotExist:
                print(f"Content for {page.page_name} not found. Loading content.")
                lang = page.language_code.replace('_', '-')
                params_parser = {
                    'action': 'parse',
                    'format': 'json',
                    'formatversion': 2,
                    'page': page.page_name,
                    'prop': 'text|images|links|sections|wikitext|parsetree'
                }
                response = requests.get(f"https://{lang}.wikipedia.org/w/api.php", params=params_parser)
                data = response.json()
                print(f"Content for {page.page_name} loaded, with {len(response.content)} bytes.")

                parser = Parser.objects.create(page=page, json=data)
                print(f"Parser for {page.page_name} created with id {parser.id}.")

            try:
                Query.objects.get(page=page)
            except Query.DoesNotExist:
                print(f"Query for {page.page_name} not found. Loading content.")
                lang = page.language_code.replace('_', '-')
                params_parser = {
                    'action': 'query',
                    'format': 'json',
                    'formatversion': 2,
                    'prop': 'revisions',
                    'titles': page.page_name,
                    'rvprop': 'ids|timestamp|user|size',
                    'rvlimit': 'max'
                }
                response = requests.get(f"https://{lang}.wikipedia.org/w/api.php", params=params_parser)
                data = response.json()
                
                while 'continue' in data:
                    print(f"Paging for {page.page_name}...")
                    params_parser['rvcontinue'] = data['continue']['rvcontinue']
                    response = requests.get(f"https://{lang}.wikipedia.org/w/api.php", params=params_parser)
                    paging_data = response.json()

                    if 'revisions' in paging_data['query']['pages'][0]:
                        data['query']['pages'][0]['revisions'].extend(paging_data['query']['pages'][0]['revisions'])

                    if 'continue' in paging_data:
                        data['continue'] = paging_data['continue']
                    else:
                        data.pop('continue', None)
                
                print(f"Content for {page.page_name} loaded, with {len(response.content)} bytes.")

                Query.objects.create(page=page, json=data)
                print(f"Query for {page.page_name} created.")
                
        print("All pages processed.")
