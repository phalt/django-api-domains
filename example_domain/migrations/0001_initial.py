import uuid

import django.contrib.postgres.fields.jsonb
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [migrations.CreateModel(
        name='Book',
        fields=[
            ('name', models.CharField(max_length=64)),
            ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False)),
            ('author_id', models.UUIDField(default=uuid.uuid4, serialize=False)),
        ],
        options={
            'abstract': False,
        },
    ),
    ]
