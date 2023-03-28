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
import queue
import threading
from rest_framework.parsers import MultiPartParser, FormParser


class FileUpload(ViewSet):
    """
    Enables file uploading for the user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FileUploadSerializer
    parser_classes = (FormParser, MultiPartParser)


    def process_file(self, job_queue):
        while not job_queue.empty():
            file = job_queue.get()
            document = Document()
            document.user_id = self.request.user
            document.file_name = str(file.name).split(".")[0]
            document.file_size = file.size
            document.file_type = "." + str(file.name).split(".")[-1]
            document.save()
            job_queue.task_done()

    def create(self, request, *args, **kwargs):

        files = request.FILES.getlist('file_uploaded')
        num_files = len(files)

        if num_files > 50:
            return Response("You can only upload up to 50 files at a time")

        job_queue = queue.Queue()
        for file in files:
            job_queue.put(file)

        # Create a thread pool
        num_threads = 10
        thread_pool = []
        for i in range(num_threads):
            t = threading.Thread(target=self.process_file, args=(job_queue,))
            t.daemon = True
            t.start()
            thread_pool.append(t)

        # wait for all threads to finish
        for t in thread_pool:
            t.join()

        return Response("All files have been uploaded")



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