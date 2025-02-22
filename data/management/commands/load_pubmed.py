from django.core.management.base import BaseCommand
from data.models import Reference
from time import sleep
import requests
import re

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for ref in Reference.objects.all():
            if not ref.pmid:
                print(f"+ Reference {ref.page.language_code} - {ref.page.page_name}")
                pmid_regex = re.search(r"(?:pmid|pubmed) *[=\|\/]? *(\d{6,8})", ref.reference, re.IGNORECASE)
                if pmid_regex:
                    pmid = pmid_regex.group(1)
                    print(f"PMID: {pmid}")
                    ref.pmid = pmid
                    ref.save()
                elif ref.doi:
                    print(f"PMID not found by regex. Trying API with DOI {ref.doi}...")
                    api = f"https://pubmed.ncbi.nlm.nih.gov/api/citmatch/?method=auto&raw-text={ref.doi}"
                    response = requests.get(api)
                    sleep(0.34)
                    if response.status_code == 200:
                        data = response.json()
                        pmid = data['result']['uids'][0]['pubmed'] if data['result']['uids'] else None
                        if pmid:
                            print(f"PMID: {pmid}")
                            ref.pmid = pmid
                            ref.save()
                        else:
                            print("PMID not found by API")
                print()
