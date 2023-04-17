from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView, View
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import *
from .models import Document
import queue
import threading
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import concurrent.futures
import time
from django.core.files.storage import FileSystemStorage
import threading
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
import time

class FileUpload(APIView):

    def get(self, request):

        return render(request, 'upload.html')

    def post(self, request):

        user = request.user
        files = request.FILES.getlist('files')

        start_time = time.time()

        # Function to handle uploading a single file
        def save_doc(file):

            storage = FileSystemStorage()
            filename = storage.save(file.name, file)
            Document.objects.create(
                user_id=user,
                file_name=str(file.name).split(".")[0],
                file_size=file.size,
                file_type="." + str(file.name).split(".")[-1],
                file_path=filename,
            )

        threads = []
        for file in files:
            thread = threading.Thread(target=save_doc, args=(file,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        elapsed_time = time.time() - start_time

        return Response({'message': 'Upload completed in {:.2f} seconds.'.format(elapsed_time)})



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