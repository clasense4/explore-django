# Generated by Django 3.0.8 on 2020-08-02 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]