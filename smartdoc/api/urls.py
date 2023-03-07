from django.urls import path
from .views import *

"""
API calls for extracting data from the databse
"""

urlpatterns = [

    # Upload a file
    path('api/upload/', FileUpload.as_view(), name='upload_file'),
    # Get all paragraphs with a given keyword 
    path('api/search?keyword=<keyword>', ParagraphByKeyword.as_view(), name='search_paragraph'),
    # Get a keyword definition
    path('api/keyword-definition?keyword=<keyword>', DefinitionByKeyword.as_view(), name='definition'),
    # Get all paragraphs with a given sentiments
    path('api/search?sentiment=<sentiment>', ParagraphBySentiment.as_view(), name='search_sentiment'),
    # Get document summary
    path('api/summary?document=<document_id>', SummaryByDocID.as_view(), name='get_summary'),
    # Get document topic
    path('api/topic?document=<document_id>', TopicByDocID.as_view(), name='get_topic'),
    # Get all location mentions within documents
    path('api/locations', Locations.as_view(), name='get_locations'),
    # Get all names in the documents
    path('api/names', Names.as_view(), name='get_names'),
    # Get all addresses in the documents
    path('api/addresses', Addresses.as_view(), name='get_addressses'),
    # Get all institution mentions within documents
    path('api/institutions', Institutions.as_view(), name='get_institutions'),
]


