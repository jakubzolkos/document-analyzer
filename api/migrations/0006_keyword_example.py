# Generated by Django 4.1.7 on 2023-04-25 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_keyword_pronunciation'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='example',
            field=models.TextField(null=True),
        ),
    ]
