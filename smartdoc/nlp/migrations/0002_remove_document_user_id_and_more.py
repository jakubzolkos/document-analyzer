# Generated by Django 4.1.7 on 2023-03-05 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nlp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='paragraph_id',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='paragraph_id',
        ),
        migrations.RemoveField(
            model_name='location',
            name='paragraph_id',
        ),
        migrations.RemoveField(
            model_name='name',
            name='paragraph_id',
        ),
        migrations.RemoveField(
            model_name='paragraph',
            name='doc_id',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='Institution',
        ),
        migrations.DeleteModel(
            name='Keyword',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Name',
        ),
        migrations.DeleteModel(
            name='Paragraph',
        ),
    ]
