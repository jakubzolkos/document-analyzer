from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


class Document(models.Model):

    user_id = models.ForeignKey(
        User, related_name="document", 
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    
    url = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )

    file_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    file_size = models.PositiveIntegerField(
        null=True, 
        blank=True
    )

    file_type = models.CharField(
        max_length=50
    )

    file_path = models.FileField(
        upload_to='documents/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    topic = models.CharField(
        max_length=255
    )

    summary = models.TextField()


class Paragraph(models.Model):
    
    doc_id = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    text = models.TextField()

    sentiment = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )


class Keyword(models.Model):
    
    paragraph_id = models.ForeignKey(
        Paragraph, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    definition = models.TextField()


class Institution(models.Model):

    paragraph_id = models.ForeignKey(
        Paragraph, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )


class Name(models.Model):
    
    paragraph_id = models.ForeignKey(
        Paragraph, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )


class Location(models.Model):
    
    paragraph_id = models.ForeignKey(
        Paragraph, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )


class Address(models.Model):
    
    paragraph_id = models.ForeignKey(
        Paragraph, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )


