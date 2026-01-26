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

            # If pmid or doi is found, try to get the rest of the data (year, cctld from source website location) from API
            if ref.pmid:
                print(f"+ Reference {ref.page.language_code} - {ref.page.page_name}")
                api = f"https://pubmed.ncbi.nlm.nih.gov/{ref.pmid}/?format=pubmed"
                response = requests.get(api)
                sleep(0.34)
                if response.status_code == 200:
                    data = response.text
                    year_regex = re.search(r"\b\d{4}\b", data)
                    year = year_regex.group(0) if year_regex else None
                    print(f"Year: {year}")
                    ref.year = year if year else 0
                    ref.save()
                else:
                    print("Error fetching data from PMID API")
                print(f"PMID: {ref.pmid}")
            elif ref.doi:
                print(f"PMID not found. Trying API with DOI {ref.doi}...")
                # Use CrossRef API to get the DOI information
                api = f"https://api.crossref.org/works/{ref.doi}"
                response = requests.get(api)
                sleep(0.34)
                if response.status_code == 200:
                    data = response.json()
                    year = data['message']['published-print']['date-parts'][0][0] if 'published-print' in data['message'] else None
                    print(f"Year: {year}")
                    ref.year = year if year else 0
                    ref.save()
                else:
                    print("Error fetching data from CrossRef API")
