from django.core.management.base import BaseCommand
from data.models import Authorship, Page
import requests, json

class Command(BaseCommand):

    def handle(self, *args, **options):
        for page in Page.objects.all():
            print(f"+ Processing page {page.language_code} - {page.page_name}")
            if Authorship.objects.filter(page=page).count() > 0:
                print(f"Authorship for {page.page_name} already done.")
            else:
                print(f"Authorship for {page.page_name} not found. Loading authorship.")
                
                lang = page.language_code.replace('_', '-')
                if lang not in ['ar', 'de', 'en',  'es',  'eu', 'fr', 'hu', 'id', 'it', 'ja', 'nl', 'pt', 'tr']:
                    print(f"Language {lang} not supported.")
                    continue

                params = {
                    'o_rev_id': 'false',
                    'editor': 'true',
                    'token_id': 'false',
                    'out': 'false',
                    'in': 'false',
                }
                response = requests.get(f"https://wikiwho.wmcloud.org/{lang}/api/v1.0.0-beta/latest_rev_content/{page.page_name}/", params=params)
                data = response.json()
                
                editor_bytes = {}
                for revision in data.get('revisions', []):
                    for rev_id, rev_data in revision.items():
                        for token in rev_data.get('tokens', []):
                            editor = "0" if token['editor'].startswith("0|") else token['editor']
                            token_str = token['str']
                            byte_count = len(token_str)
                            if editor in editor_bytes:
                                editor_bytes[editor] += byte_count
                            else:
                                editor_bytes[editor] = byte_count
                
                print(f"Authorship for {page.page_name} loaded, with {len(response.content)} bytes.")
                print(f"Editor byte counts: {json.dumps(editor_bytes, indent=2)}")

                for editor, byte_count in editor_bytes.items():
                    authorship = Authorship.objects.create(page=page, language_code=lang, author=editor, size=byte_count)
                    print(f"Authorship for {page.page_name} created with id {authorship.id}.")

