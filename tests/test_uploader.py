import pytest
import django
from django.urls import reverse
from api.models import Document, Paragraph, Keyword
from django.core.files.uploadedfile import SimpleUploadedFile
from api.serializers import DocumentSerializer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import os

django.setup()

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(email='test@example.com', password='testpassword')


@pytest.fixture
def authenticated_api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.mark.django_db
def test_documents_view_get(authenticated_api_client):
    response = authenticated_api_client.get(reverse('documents'))
    assert response.status_code == 200
    assert 'files' in response.context

@pytest.mark.django_db
def test_documents_view_post(authenticated_api_client, user):
    
    content = b"This is a template sentence. It is used for testing"
    file = SimpleUploadedFile("test_file.txt", content)
    response = authenticated_api_client.post(reverse('documents'), {'files': file}, format='multipart')
    assert response.status_code == 200
    document = Document.objects.filter(user_id=user).first()
    assert document is not None
    assert document.file_name == 'test_file'

@pytest.mark.django_db
def test_delete_view(authenticated_api_client, user):
    document = Document.objects.create(
        user_id=user,
        file_name="test_file",
        file_size=10,
        file_type=".txt",
        file_path="test_file.txt",
        topic="Test topic",
        summary="Test summary"
    )
    response = authenticated_api_client.post(reverse('delete'), {'filename': 'test_file'})
    assert response.status_code == 302
    assert '/api/upload' in response.url
    document_exists = Document.objects.filter(user_id=user, file_name='test_file').exists()
    assert document_exists is False

@pytest.mark.django_db
def test_rename_view(authenticated_api_client, user):
    document = Document.objects.create(
        user_id=user,
        file_name="test_file",
        file_size=10,
        file_type=".txt",
        file_path="test_file.txt",
        topic="Test topic",
        summary="Test summary"
    )
    response = authenticated_api_client.post(reverse('rename'), {'filename': 'test_file', 'new_filename': 'new_test_file'})
    assert response.status_code == 302
    assert '/api/upload' in response.url
    document.refresh_from_db()
    assert document.file_name == 'new_test_file'