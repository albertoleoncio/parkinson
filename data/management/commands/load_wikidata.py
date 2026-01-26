from django.core.management.base import BaseCommand
from data.models import Category
import requests

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        psid = options['psid']
        petscan_url = f'https://petscan.wmcloud.org/?psid={psid}&format=json'
        response = requests.get(petscan_url)
        data = response.json()
        for article in data['*'][0]['a']['*']:
            article_id = article['id']
            article_name = article['title']
            article_wikidata = article['metadata']['wikidata']
            category, created = Category.objects.get_or_create(article_id=article_id, article_name=article_name, article_wikidata=article_wikidata)

        # Check if there are old articles on database that are not on the new list
        old_articles = Category.objects.all()
        for article in old_articles:
            found = False
            for new_article in data['*'][0]['a']['*']:
                if article.article_id == new_article['id']:
                    found = True
                    break
            if not found:
                article.delete()
    
