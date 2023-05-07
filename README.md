# Document Analyzer 
[IN PROGRESS]
Written by Jakub Zolkos for EC 530: Software Engineering Principles 
## Table of Contents

- [Introduction](#introduction)
- [Database](#database)
- [Installation](#installation)
- [Application Usage](#apptutorial)
- [Standalone NLP API](#nlpapi)
- [Not Yet Implemented](#issues)




## Introduction
Document analyzer API that provides multiple text analysis features. Written using Django REST Framework.

## Database

### Design Rationale
Database design is a crucial factor when implementing any web application. The most important question is the type of the database, which can be SQL-based or noSQL, such as MongoDB. For the purpose of this application, an SQL implementation was chosen due to the following reasons:

- Necessary data can be stored using a stable schema and is naturally relational
- The application database doesn't need to store significant amount of data
- Easy to use with Django object relational mapping

### Overview 

- User table containing login credentials of registered users
- Document table with various metadata and one-to-many relationship between the user and a document
- URL field if the text was obtained from an external website rather than an uploaded file
- Summary and topic of the document for easy future search
- Paragraph table with one-to-many relationship between a document and paragraphs, text and sentiment
- No text column necessary in the Document table, as each document is comprised of paragraphs - more precise access
- Tables with locations, addresses, names and institutions 
- Keyword tables with names and definitions obtained from external website - creating a new document will mark each paragraph within a document with appropriate keyword tags

![Database](https://github.com/ECE530-2023/news-analyzer-jakubzolkos/blob/main/backend/assets/database.png)

## Installation
1. Clone the repository
```
git clone https://github.com/ECE530-2023/unit-test-jakubzolkos
```
2. Install virtual environment (if not installed already)
```
pip install virtualenv
```
3. Create and activate virtual environment
```
virtualenv venv
source venv/bin/activate
```
4. Install prerequisites
```
pip install -r requirements.txt
```
6. Navigate to the root folder and run the application server
```
python3 manage.py runserver
```

## Application Usage Tutorial
After opening the server, you can sign-up with a new account or log into an existing account. A custom authorization model is used that enables registering new users with only an email address and a password (authentication/models.py). The Google authentication and password recovery options are currently unavailable. Authenticated user will obtain a session token that lasts 30 minutes, unless the user logs out of the account and deletes browser cookies. 


## Standalone NLP API
While the application uses a generic implementation of the natural language processing functionalities, an API is also available for users who want to use them in external applications. You can find the API in the nlpapi.py file. This API provides a set of endpoints for processing and analyzing documents. The supported file formats include PDF, JPG, PNG, DOC, and DOCX. Many of the endpoints support an optional text argument that allows performing analysis on text string data instead of a file. This allows for easy use of different analysis combinations. Functionalities:

- Extract text from a document
- Extract the main topic of a document
- Summarize a document
- Extract definitions for a given word
- Perform sentiment analysis

### Installation

To run the FastAPI application, install FastAPI and an ASGI server like Uvicorn with the following command:
```
pip3 install fastapi uvicorn
```
### Running the API

Save your FastAPI application code in a Python file, e.g., main.py. Then, open a terminal or command prompt, navigate to the directory containing main.py, and run the following command:
```
uvicorn nlpapi:app --reload
```
By default, the API will be accessible at http://127.0.0.1:8000. You can view the interactive API documentation at http://127.0.0.1:8000/docs.

### Endpoints

#### Extract Text

- **URL**: `/extract_text/`
- **Method**: `POST`
- **Authentication**: `Token`
- **Data Params**: `file=[multipart/form-data]`
- **Success Response**: `{"text": "Extracted text"}`

#### Extract Topic

- **URL**: `/extract_topic/`
- **Method**: `POST`
- **Authentication**: `Token`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string], num_topics=[int], num_words=[int]`
- **Success Response**: `{"topic": ["word1", "word2", "word3"]}`

#### Summarize Text

- **URL**: `/summarize_text/`
- **Method**: `POST`
- **Authentication**: `Token`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string], per=[float]`
- **Success Response**: `{"summary": "Text summary"}`

#### Extract Definitionsg

- **URL**: `/extract_definitions/`
- **Method**: `GET`
- **Authentication**: `Token`
- **Query Params**: `word=[string]`
- **Success Response**: `{"part_of_speech": "noun", "definition": "A brief description", "pronunciation": "example", "example": "An example sentence"}`

#### Perform Sentiment Analysis

- **URL**: `/perform_sentiment_analysis/`
- **Method**: `POST`
- **Authentication**: `Token`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string]`
- **Success Response**: `{"sentiments": ["Very Positive", "Neutral", "Negative"]}`

#### Divide into Paragraphs

- **URL**: `/divide_into_paragraphs/`
- **Method**: `POST`
- **Authentication**: `Token`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string]`
- **Success Response**: `{"paragraphs": ["Paragraph 1", "Paragraph 2", "Paragraph 3"]}`

#### Tag Keywords

- **URL**: `/tag_keywords/`
- **Method**: `POST`
- **Authentication**: `Token`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string]`
- **Success Response**: `{"keywords": [["word1", "word2"], ["word3", "word4"], ["word5", "word6"]]}`

#### Process File

- **URL**: `/process_file/`
- **Method**: `POST`
- **Authentication**: `Token`
- **Data Params**: `file=[multipart/form-data]`
- **Success Response**: `{"topic": "Main topic", "summary": "Text summary", "paragraphs": [{"text": "Paragraph 1", "sentiment": "Very Positive", "keywords": ["word1", "word2"]}, {"text": "Paragraph 2", "sentiment": "Neutral", "keywords": ["word3", "word4"]}, {"text": "Paragraph 3", "sentiment": "Negative", "keywords": ["word5", "word6"]}]}`


### Example Usage

#### Extract Text

```bash
curl -X POST "http://127.0.0.1:8000/extract_text/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/file.pdf"
```

## Not Implemented Yet
- Google authentication and password recovery
- Document preview and analysis download
- Settings and Help tabs
