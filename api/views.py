from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView, View
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import *
from .models import *
import queue
import os
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
from datetime import datetime
from fuzzywuzzy import process


class DocumentsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        documents = Document.objects.filter(user_id=request.user)
        payload = DocumentSerializer(documents, many=True).data
        return render(request, 'upload.html', context={'files': payload})

    def post(self, request):

        def save_data(file):

            # Obtain files and analysis
            storage = FileSystemStorage()
            filename = storage.save(file.name, file)
            filepath = os.path.join(os.getcwd(), "media", file.name)
            from nlp.api import NLP_API
            import json
            nlp = NLP_API()
            nlp.process_file(filepath)
            analysis = json.loads(nlp.to_json())

            # Create document
            document = Document.objects.create(
                user_id=request.user,
                file_name=str(file.name).split(".")[0],
                file_size=file.size,
                file_type="." + str(file.name).split(".")[-1],
                file_path=filename,
                topic=analysis['topic'],
                summary=analysis['summary'],
            )

            for paragraph in analysis['paragraphs']:

                new_paragraph = Paragraph.objects.create(

                    doc_id=document,
                    text=paragraph['text'],
                    sentiment=paragraph['sentiment'],
                )

                for keyword, metadata in paragraph['keywords'].items():
      
                    if metadata is not None:
                        
                        try:
                            word = Keyword.objects.get(word=keyword)
                            
                        except:

                            word = Keyword(

                            word=keyword,
                            part_of_speech=metadata['part_of_speech'],
                            definition=metadata['definition'],
                            pronunciation=f"/{metadata['pronunciation']}/",
                            example=metadata['example']
                            ) 

                            word.save()

                        finally:   

                            word.users.add(request.user)
                            word.paragraphs.add(new_paragraph)
                            word.save()
                
                
        files = request.FILES.getlist('files')
        if len(files) > 1:
            threads = []
            for file in files:
                if not Document.objects.filter(user_id=request.user, file_name=str(file.name).split(".")[0]):
                    thread = threading.Thread(target=save_data, args=(file,))
                    thread.start()
                    threads.append(thread)

            for thread in threads:
                thread.join()

        else:
            save_data(files[0])

        return self.get(request)


class DeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        file_name = request.POST["filename"]
        target_file = Document.objects.filter(user_id=request.user, file_name = file_name)
        target_file.delete()

        return redirect("documents")

class RenameView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        file_name, new_name = request.POST["filename"], request.POST["new_filename"]
        target_file = Document.objects.filter(user_id=request.user, file_name = file_name)[0]  
        target_file.file_name = new_name
        target_file.save()

        return redirect("documents")


class AnalyticsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        mode = request.GET.get('mode')
        word = request.GET.get('keywords')
        
        if mode == "Dictionary" or mode is None:

            user_keywords = Keyword.objects.filter(users=request.user).order_by('word')

            if word is not None and word != "":

                # Extract a list of words from the user's keywords
                user_keywords_list = [k.word for k in user_keywords]
                matches = process.extract(word, user_keywords_list, limit=None)
                similarity_threshold = 80
                similar_words = [match[0] for match in matches if match[1] >= similarity_threshold]

                user_keywords = user_keywords.filter(word__in=similar_words).order_by('word')
        
            return render(request, 'analytics.html', context={"keywords": user_keywords})
        
        elif mode == "Paragraphs":

            sentiment = request.GET.get('range')
            paragraphs = Paragraph.objects.filter(doc_id__user_id=request.user)
            
            if word != "":

                # Get all paragraphs belonging to user's documents that contain the keywords
                keywords = [w.strip() for w in word.split(',')]
                paragraphs = Paragraph.objects.filter(doc_id__user_id=request.user)
                paragraphs = paragraphs.filter(keywords__word__in=keywords)

            if sentiment == "Neutral":
                paragraphs = paragraphs.filter(sentiment="Neutral")
            elif sentiment == "Positive":
                paragraphs = paragraphs.filter(sentiment__in=["Positive", "Very Positive"])
            elif sentiment == "Negative":
                paragraphs = paragraphs.filter(sentiment__in=["Negative", "Very Negative"])

            return render(request, 'analytics.html', context={'paragraphs': paragraphs})

        return render(request, 'analytics.html')


class DefinitionByKeyword(APIView):
    """
    Returns the definition of the input keyword
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        query = request.GET.get('word')
        # Filter keywords by authenticated user
        user_keywords = Keyword.objects.filter(users=request.user)

        # Apply the search query if provided
        if query is not None and query != "view_all":
            # Extract a list of words from the user's keywords
            user_keywords_list = [k.word for k in user_keywords]

            # Get a list of matches using the fuzzywuzzy library
            matches = process.extract(query, user_keywords_list, limit=None)

            # Set a similarity threshold (0-100, higher means more similar)
            similarity_threshold = 75

            # Filter the matches that have a similarity score above the threshold
            similar_words = [match[0] for match in matches if match[1] >= similarity_threshold]

            # Update the user_keywords queryset to include only similar words
            user_keywords = user_keywords.filter(word__in=similar_words)

        # Order the results
        user_keywords = user_keywords.order_by('word')
        
        return render(request, 'dictionary.html', context={"keywords": user_keywords})


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