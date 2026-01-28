from django.db import models

# Create your models here.

class Category(models.Model):
    article_id = models.IntegerField(unique=True)
    article_name = models.CharField(max_length=200)
    article_wikidata = models.CharField(max_length=200)

    def __str__(self):
        return self.article_name

class Page(models.Model):
    referer = models.ForeignKey(Category, on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    page_name = models.CharField(max_length=200)
    page_url = models.URLField()

    def __str__(self):
        return self.language_code + ' - ' + self.referer.article_name

    class Meta:
        unique_together = ('referer', 'language_code')

class Parser(models.Model):
    page = models.OneToOneField(Page, on_delete=models.CASCADE)
    json = models.JSONField()

    def __str__(self):
        return self.page.language_code + ' - ' + self.page.referer.article_name

class Query(models.Model):
    page = models.OneToOneField(Page, on_delete=models.CASCADE)
    json = models.JSONField()

    def __str__(self):
        return self.page.language_code + ' - ' + self.page.referer.article_name

class Analysis(models.Model):
    page = models.OneToOneField(Page, on_delete=models.CASCADE)
    words = models.IntegerField()
    images = models.IntegerField()
    intrawikis = models.IntegerField()
    sections = models.IntegerField()
    total_edits = models.IntegerField()
    first_edit = models.DateTimeField()
    last_edit = models.DateTimeField()
    unique_editors = models.IntegerField()
    
    def __str__(self):
        return self.page.language_code + ' - ' + self.page.referer.article_name

class Reference(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    reference = models.TextField()
    year = models.IntegerField(blank=True)
    cctld = models.CharField(max_length=10, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    pmid = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.page.language_code + ' - ' + self.page.referer.article_name + ' - ' + self.id

class Authorship(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    author = models.CharField(max_length=200)
    size = models.IntegerField()

    def __str__(self):
        return self.page.language_code + ' - ' + self.page.referer.article_name

class Pageviews(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    views = models.IntegerField()

    def __str__(self):
        return self.page.language_code + ' - ' + self.page.referer.article_name + ' - ' + str(self.date)