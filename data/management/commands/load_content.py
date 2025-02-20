from django.core.management.base import BaseCommand
from data.models import Page, Content
import requests

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for page in Page.objects.all():
            lang = page.language_code.replace('_', '-')
            response = requests.get(f"https://{lang}.wikipedia.org/w/api.php?action=parse&format=json&prop=parsetree&formatversion=2&page={page.page_name}")
            data = response.json()
            if 'parse' in data:
                content = data['parse']['parsetree']
                try:
                    Content.objects.get(page=page, content=content)
                    print(f"Content for {lang} - {page.page_name} already exists")
                except Content.DoesNotExist:
                    Content.objects.create(page=page, content=content)
                    print(f"Added content for {lang} - {page.page_name}")
            else:
                print(f"Skipping {lang} - {page.page_name}")
