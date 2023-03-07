from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import HttpResponse


class FileUpload(APIView):
    """
    Enables file uploading for the user
    """
    def post(self, request, *args, **kwargs):
        return HttpResponse("This is a POST request.")


class ParagraphByKeyword(APIView):
    """ 
    Finds all paragraphs that contain a given keyword
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")


class ParagraphBySentiment(APIView):
    """ 
    Finds all paragraphs with a given sentiment
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")


class DefinitionByKeyword(APIView):
    """
    Returns the definition of the input keyword
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")


class SummaryByDocID(APIView):
    """ 
    Returns the summary of a document with a given ID
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")


class TopicByDocID(APIView):
    """ 
    Returns the topic of a document with a given ID
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")


class Institutions(APIView):
    """
    Return the list of all institutions in the documents
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")


class Locations(APIView):
    """
    Return the list of all locations in the documents
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")


class Addresses(APIView):
    """
    Return the list of all addresses in the documents
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")    


class Names(APIView):
    """
    Return the list of all names in the documents
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is a GET request.")    