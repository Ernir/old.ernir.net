from blog.managers import TagByCountManager
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Tag(models.Model):
    """

    A tag, grouping many entries together.
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField()

    objects = models.Manager()
    objects_by_entry_count = TagByCountManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Entry(models.Model):
    """

    A blog entry.
    """

    title = models.CharField(max_length=400)
    body = models.TextField()
    published = models.DateTimeField()

    slug = models.SlugField()
    excerpt = models.CharField(max_length=400)
    tags = models.ManyToManyField(Tag, related_name="entries")

    # Tiny little language association for each article.
    _is = "IS"
    _en = "EN"
    _language_choices = (
        (_is, "Icelandic"),
        (_en, "English")
    )
    language = models.CharField(
        max_length=2,
        choices=_language_choices,
        default=_en
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "entries"
        ordering = ("-published", )


class Comment(models.Model):
    """

    A comment on a blog entry.
    """

    content = models.TextField()
    published = models.DateTimeField()
    associated_with = models.ForeignKey(Entry, related_name="comments")
    author = models.ForeignKey(User)

    def __str__(self):
        return self.author.username + " at " + str(self.published)