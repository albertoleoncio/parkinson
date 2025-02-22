from django.core.management.base import BaseCommand
from data.models import Parser, Reference
from xml.etree import ElementTree
import re

class Command(BaseCommand):

    def handle(self, *args, **options):
        for content in Parser.objects.all():
            print(f"+ Reference {content.page.language_code} - {content.page.page_name}")
            tree = ElementTree.fromstring(content.json.get("parse", {}).get("parsetree", {}))
            for ext in tree.findall(".//ext[name='ref']"):
                inner = ext.find("inner")
                if inner is None or inner.text is None:
                    continue

                url = re.search(r'(https?://[^\s]+)', inner.text)
                year = re.search(r'20[012]\d', inner.text)
                cctld = re.search(r'(?<=\.)[a-z]+(?=\/)', url.group(0)) if url else None
                doi = re.search(r'10\.\d{4,9}\/[-._;()/:a-zA-Z0-9]+', inner.text)

                Reference.objects.create(
                    page=content.page,
                    reference=inner.text,
                    year=year.group(0) if year else 0,
                    cctld=cctld.group(0) if cctld else '',
                    doi=doi.group(0) if doi else ''
                )
                print(f"Reference: {inner.text}")
                print(f"Year: {year.group(0) if year else ''}")
                print(f"CCTLD: {cctld.group(0) if cctld else ''}")
                print(f"DOI: {doi.group(0) if doi else ''}")
                print()