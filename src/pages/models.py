from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField()
    language = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)
