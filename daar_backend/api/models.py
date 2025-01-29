from django.db import models

class BookCompact(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    authors = models.JSONField()
    subjects = models.JSONField()
    bookshelves = models.JSONField()
    languages = models.JSONField()
    copyright = models.BooleanField(default=False)
    media_type = models.CharField(max_length=50)
    download_count = models.IntegerField(default=0)
    text_content = models.TextField(null=True, blank=True) # TOUT le contenu
    cover_url = models.URLField(null=True, blank=True)

    # pour recherche
    centrality = models.FloatField(null=True, blank=True)
    neighbors = models.JSONField(null=True, blank=True) 

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title