from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import *
from rest_framework.viewsets import ViewSet
from django.core.files.storage import FileSystemStorage
from .models import Document

class FileUpload(ViewSet):
    """
    Enables file uploading for the user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FileUploadSerializer

    def create(self, request, *args, **kwargs):

        file = request.FILES.get('file_uploaded')
        document = Document()
        document.user_id = request.user
        document.file_name = str(file.name).split(".")[0]
        document.file_size = file.size
        document.file_type = "." + str(file.name).split(".")[-1]
        document.save()

        response = "You have uploaded a {} file".format(document.file_name)
        return Response(response)


class DocumentList(APIView):
    """
    Shows the names of all the uploaded files
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        documents = Document.objects.filter(user_id=user)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

class ParagraphByKeyword(APIView):
    """ 
    Finds all paragraphs that contain a given keyword
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response)


class ParagraphBySentiment(APIView):
    """ 
    Finds all paragraphs with a given sentiment
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response)


class DefinitionByKeyword(APIView):
    """
    Returns the definition of the input keyword
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response)


class SummaryByDocID(APIView):
    """ 
    Returns the summary of a document with a given ID
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response)


class TopicByDocID(APIView):
    """ 
    Returns the topic of a document with a given ID
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response)


class Institutions(APIView):
    """
    Return the list of all institutions in the documents
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response)


class Locations(APIView):
    """
    Return the list of all locations in the documents
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response)


class Addresses(APIView):
    """
    Return the list of all addresses in the documents
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response) 


class Names(APIView):
    """
    Return the list of all names in the documents
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = "Not implemented yet :)"
        return Response(response)