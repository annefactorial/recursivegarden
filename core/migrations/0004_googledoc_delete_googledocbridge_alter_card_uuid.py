# Generated by Django 4.0.5 on 2022-07-17 20:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_card_url_alter_googledocbridge_google_doc_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_doc_title', models.CharField(max_length=1023)),
                ('google_doc_url', models.CharField(max_length=1023)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='GoogleDocBridge',
        ),
        migrations.AlterField(
            model_name='card',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='A universally unique identifier, allows referencing a card if no url is provided.', unique=True),
        ),
    ]
