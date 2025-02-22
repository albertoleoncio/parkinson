from django.core.management.base import BaseCommand
from data.models import Parser, Analysis, Query
from xml.etree import ElementTree
from bs4 import BeautifulSoup

class Command(BaseCommand):

    def handle(self, *args, **options):
        for parser in Parser.objects.all():
            try:
                Analysis.objects.get(page=parser.page)
                continue
            except Analysis.DoesNotExist:
                pass

            print(f"+ Parser {parser.page.language_code} - {parser.page.page_name}")
            data = parser.json.get("parse", [])

            images = len(data.get("images", []))
            intrawikis = sum(1 for link in data.get("links", []) if link.get("ns") == 0 and link.get("exists"))
            sections = sum(1 for section in data.get("sections", []) if section.get("toclevel") == 1)
            text = BeautifulSoup(data.get("text", {}), "html.parser").get_text().split()
            words = len(text)

            print(f"Images: {images}")
            print(f"Intrawikis: {intrawikis}")
            print(f"Sections: {sections}")
            print(f"Words: {words}")


            query = Query.objects.get(page=parser.page)
            data_query = query.json.get("query")
            
            total_edits = len(data_query.get("pages")[0].get("revisions"))
            first_edit = data_query.get("pages")[0].get("revisions")[-1].get("timestamp")
            last_edit = data_query.get("pages")[0].get("revisions")[0].get("timestamp")
            unique_editors = len(set(revision.get("user") for revision in data_query.get("pages")[0].get("revisions")))

            print(f"Total edits: {total_edits}")
            print(f"First edit: {first_edit}")
            print(f"Last edit: {last_edit}")
            print(f"Unique editors: {unique_editors}")
            
            Analysis.objects.create(
                page=parser.page,
                words=words,
                images=images,
                intrawikis=intrawikis,
                sections=sections,
                total_edits=total_edits,
                first_edit=first_edit,
                last_edit=last_edit,
                unique_editors=unique_editors
            )

        # TODO:
        # Quantidade de palavras, imagens, intrawikis e seções
        # Referências: quantidade, ano, idioma(?)
        # Referências com DOI: quantidade, ano, idioma, publisher->pubmed(?)
        # Histórico do artigo: data da primeira e da última edição, quantidade de edições, quantidade de editores
        # Análise de autoria: WhoWroteThat por idioma

        # Comparativo com outras doenças: Alzheimer e Tourette
        # Refazer a mesma análise feita para o Parkinson