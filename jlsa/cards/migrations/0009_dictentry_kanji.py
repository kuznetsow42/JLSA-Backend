# Generated by Django 5.1.4 on 2025-01-08 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_radical_kanji'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictentry',
            name='kanji',
            field=models.ManyToManyField(related_name='words', to='cards.kanji'),
        ),
    ]
