import uuid

from django.db import models


class Book(models.Model):

    id = models.UUIDField(primar_key=True, default=uuid.uuid4)
    name = models.BooleanField(default=False)
    author_id = models.UUIDField(default=uuid.uuid4)
