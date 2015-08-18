from django.db import models


class Section(models.Model):
    """

    One section of the index page.
    """
    title = models.CharField(max_length=200)
    text = models.TextField()

    priority = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("priority", )


class SubSection(models.Model):
    """

    One subsection of the index page.
    """

    title = models.CharField(max_length=200)
    text = models.TextField()
    parent_section = models.ForeignKey(Section, related_name="subsections")

    priority = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("priority", )