# Generated by Django 5.0.1 on 2024-01-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecturespaces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='title',
            field=models.CharField(default='Default Title', max_length=200),
        ),
    ]
