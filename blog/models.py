from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Tag(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Entry(models.Model):

    title = models.CharField(max_length=200)
    body = models.TextField()
    published = models.DateTimeField()

    slug = models.SlugField()
    excerpt = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.excerpt = self.body[0:100]  # first 100 chars
        super(Entry, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "entries"
        ordering = ("published", )


class Comment(models.Model):

    content = models.TextField()
    published = models.DateTimeField()
    associated_with = models.ForeignKey(Entry, related_name="comments")
    author = models.ForeignKey(User)

    def __str__(self):
        return self.author.username + " at " + str(self.published)