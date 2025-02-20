from django.core.management.base import BaseCommand
from data.models import Category, Page
import requests

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for page in Category.objects.all():
            print(page.article_name)
            wikidata_id = page.article_wikidata
            wikidata_url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks%2Furls%7Csitelinks&formatversion=2&ids={wikidata_id}"
            response = requests.get(wikidata_url)
            data = response.json()
            if 'sitelinks' in data['entities'][wikidata_id]:
                for key, value in data['entities'][wikidata_id]['sitelinks'].items():
                    if key.endswith('wiki') and key != 'commonswiki':
                        language_code = key.replace('wiki', '')
                        page_name = value['title']
                        page_url = value['url']
                        Page.objects.create(referer=page, language_code=language_code, page_name=page_name, page_url=page_url)
                        print(f"Added page {page_name} in {language_code}")
                    else:
                        print(f"Skipping {key}")
            else:
                print(f"Skipping {page.article_name}")
