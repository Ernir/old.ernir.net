from django.db import models


class VtPFile(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=400)
    released = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-released", )