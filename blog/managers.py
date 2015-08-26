from django.db import models
from django.db.models import Count


class TagByCountManager(models.Manager):
    """
    Defines a queryset ordered by the number of blog entries with which
    this tag is associated.
    """

    def get_queryset(self):
        return super(TagByCountManager, self). \
            get_queryset().annotate(num_tags=Count("entries")).\
            order_by("-num_tags", "name")