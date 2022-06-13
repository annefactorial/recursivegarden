from django.db import models
from django.utils import timezone
from uuid import uuid4


class Room(models.Model):
    domain_name = models.CharField(max_length=255)

