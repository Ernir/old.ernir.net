from django.db import models


class VtPFile(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=400)
    released = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-released", )


class Chapter(models.Model):
    title = models.CharField(max_length=200)
    first_text = models.TextField()
    filepath = models.CharField(max_length=200, blank=True, default="")

    order = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("order", )


class Section(models.Model):
    title = models.CharField(max_length=200)
    first_text = models.TextField()
    parent = models.ForeignKey(Chapter)

    order = models.IntegerField()

    def __str__(self):
        return self.parent.title + ": " + self.title

    class Meta:
        ordering = ("parent__order", "order", )


class Subsection(models.Model):
    title = models.CharField(max_length=200)
    first_text = models.TextField()
    parent = models.ForeignKey(Section)

    order = models.IntegerField()

    def __str__(self):
        return self.parent.title + ": " + self.title

    class Meta:
        ordering = ("parent__parent__order", "parent__order", "order", )


class Subsubsection(models.Model):
    title = models.CharField(max_length=200)
    first_text = models.TextField()
    parent = models.ForeignKey(Subsection)

    order = models.IntegerField()

    def __str__(self):
        return self.parent.title + ": " + self.title

    class Meta:
        ordering = (
            "parent__parent__parent__order",
            "parent__parent__order",
            "parent__order", "order",
        )