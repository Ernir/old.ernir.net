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
    parent = models.ForeignKey(Chapter, on_delete=models.PROTECT)

    order = models.IntegerField()

    def __str__(self):
        return self.parent.title + ": " + self.title

    class Meta:
        ordering = ("parent__order", "order", )


class Subsection(models.Model):
    title = models.CharField(max_length=200)
    first_text = models.TextField()
    parent = models.ForeignKey(Section, on_delete=models.PROTECT)

    order = models.IntegerField()

    def __str__(self):
        return self.parent.title + ": " + self.title

    class Meta:
        ordering = ("parent__parent__order", "parent__order", "order", )


class Subsubsection(models.Model):
    title = models.CharField(max_length=200)
    first_text = models.TextField()
    parent = models.ForeignKey(Subsection, on_delete=models.PROTECT)

    order = models.IntegerField()

    def __str__(self):
        return self.parent.title + ": " + self.title

    class Meta:
        ordering = (
            "parent__parent__parent__order",
            "parent__parent__order",
            "parent__order", "order",
        )


class Spell(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)


class CharacterClass(models.Model):
    short_name = models.CharField(max_length=200)
    long_name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()
    is_new = models.BooleanField(default=False)

    class_types = (
        ("base", "Base Class"),
        ("prestige", "Prestige Class"),
        ("npc", "NPC Class")
    )

    class_type = models.CharField(max_length=20, choices=class_types)

    def __str__(self):
        return self.short_name

    class Meta:
        ordering = ("short_name",)