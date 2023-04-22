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


class DocumentsView(APIView):

    def get(self, request):

        user = request.user
        documents = Document.objects.filter(user_id=user)
        paylod = DocumentSerializer(documents, many=True).data
        return render(request, 'upload.html', context={'files': paylod})

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

        return self.get(request)


class DeleteView(APIView):

    def post(self, request):
        
        file_name = request.POST["filename"]
        target_file = Document.objects.filter(user_id=request.user, file_name = file_name)
        target_file.delete()

        return redirect("documents")

class RenameView(APIView):

    def post(self, request):
        
        file_name, new_name = request.POST["filename"], request.POST["new_filename"]
        target_file = Document.objects.filter(user_id=request.user, file_name = file_name)[0]  
        target_file.file_name = new_name
        target_file.save()

        return redirect("documents")


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