from django.db import models


class Section(models.Model):
    """

    One section of the index page.
    """
    title = models.CharField(max_length=200)
    text = models.TextField()

    priority = models.IntegerField()

    def __str__(self):
        return self.title + " (priority:" + str(self.priority) + ")"

    class Meta:
        ordering = ("priority", )


class SubSection(models.Model):
    """

    One subsection of the index page.
    """

    title = models.CharField(max_length=200)
    text = models.TextField(null=True)
    parent_section = models.ForeignKey(Section, related_name="subsections")

    priority = models.IntegerField()

    def __str__(self):
        return self.parent_section.title + ": " \
               + self.title + " (priority:" + str(self.priority) + ")"

    class Meta:
        ordering = ("parent_section__priority", "priority", )