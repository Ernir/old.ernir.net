from django.db import models

# Create your models here.


class Entry(models.Model):

    title = models.CharField(max_length=200)
    body = models.TextField()
    published = models.DateTimeField()


class Comment(models.Model):

    content = models.TextField()
    published = models.DateTimeField()
    associated_with = models.ForeignKey(Entry)