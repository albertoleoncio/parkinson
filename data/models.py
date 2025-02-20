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

class Content(models.Model):
    page = models.OneToOneField(Page, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.page.language_code + ' - ' + self.page.referer.article_name
