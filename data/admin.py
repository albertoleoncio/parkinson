from django.contrib import admin
from .models import Category, Page, Parser, Query, Analysis, Reference, Authorship

# Register your models here.
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Parser)
admin.site.register(Query)
admin.site.register(Analysis)
admin.site.register(Reference)
admin.site.register(Authorship)