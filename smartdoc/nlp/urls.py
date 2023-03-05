from django.urls import path

"""
API calls for performing analysis on the uploaded documents 
"""

# urlpatterns = [
#     # Extract text from an uploaded document specified with a path
#     path('/nlp/extract-text?filepath=<path>', name="extract_text"),
#     # Tags the documents and paragraphs within given range with keywords
#     path('/nlp/tag?documents=<range>', name="tag_documents"),
#     # Performs sentiment analysis 
#     path('/nlp/sentiment-analyze?documents=<range>', name="get_sentiment"),
#     # Get keyword definition from outside source
#     path('/nlp/search-definitions?keyword?<keyword>', name="get_keyword_definitions"),
#     # Get a summary of a document
#     path('/nlp/summarize?document=<document_id>', name="get_summary"),
#     # Search outside sources for keywords (sources predefined)
#     path('/nlp/search-keyword-online?source=<source>', name="search_keyword_online")
# ]



