from django.core.management.base import BaseCommand
from data.models import Content
from xml.etree import ElementTree

class Command(BaseCommand):

    def handle(self, *args, **options):
        for content in Content.objects.all():
            # Parse XML content
            tree = ElementTree.fromstring(content.content)
            # Find all references "<ext><name>ref</name><attr>...</attr><inner>...</inner></ext>", where attr and inner are optional
            for ext in tree.findall(".//ext[name='ref']"):
                # Find the attribute of the reference
                attr = ext.find("attr")
                # Find the inner text of the reference
                inner = ext.find("inner")
                if attr is not None:
                    print(f"Reference {attr.text}")
                if inner is not None:
                    print(f"Reference {inner.text}")
