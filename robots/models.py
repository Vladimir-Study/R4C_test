import random
from django.db import models


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False, default=random.randint(1,1000000000))
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
