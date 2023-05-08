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

![Database](https://github.com/jakubzolkos/document-analyzer/blob/main/assets/database.png)

## Installation
1. Clone the repository
```
git clone https://github.com/jakubzolkos/document-analyzer
```
2. Install virtual environment (if not installed already)
```
pip3 install virtualenv
```
3. Create and activate virtual environment
```
virtualenv venv
source venv/bin/activate
```
4. Install prerequisites
```
pip3 install -r requirements.txt
```
6. Navigate to the root folder and run the application server
```
python3 manage.py runserver
```

## Application Usage Tutorial
### Login
After opening the server, you can sign-up with a new account or log into an existing account. A custom authorization model is used that enables registering new users with only an email address and a password (authentication/models.py). The Google authentication and password recovery options are currently unavailable. Authenticated user will obtain a session token that lasts 30 minutes, unless the user logs out of the account and deletes browser cookies. 

![Login](https://github.com/jakubzolkos/document-analyzer/blob/main/assets/login.png)

### File Uploading and Document View
After a successful login, the user will be redirected to a dashboard. A navigation bar on the left contains multiple tabs: documents, analytics, setting and help; the last two are currently unavailable. In the documents tab, the user will be able to view all uploaded files, change their name, delete them or download the file (not yet implemented). A green button in the top right corner enables the user to upload multiple files at the same time. Uploading a new file will trigger a POST request during which the API will perform full analysis of the file and save the result to a database (see standalone NLP API in the section below). Currently no progress bar has been implemented, therefore, the request progress is indicated by the rotating tab circle. An upload is successful if new files appear in the document view.

![Login](https://github.com/jakubzolkos/document-analyzer/blob/main/assets/upload.png)

### Analytics

In the analytics tab the user is able to view the data extracted from the uploaded files. Currently, two options are implemented: keyword dictionary and extracted paragraphs with sentiments analysis. In the keyword dictionary, the user can search for desired keywords in a textbox and the API will return a set of keywords that most closely match the desired keyword. In the paragraph view, the user can see all the extracted paragraphs and filter paragraphs based on their sentiments.

![Dictionary](https://github.com/jakubzolkos/document-analyzer/blob/main/assets/dictionary.png)
![Paragraphs](https://github.com/jakubzolkos/document-analyzer/blob/main/assets/paragraphs.png)



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

#### Extract Definitions

- **URL**: `/extract_definitions/`
- **Method**: `GET`
- **Query Params**: `word=[string]`
- **Success Response**: `{"part_of_speech": "noun", "definition": "a word definition", "pronunciation": "pronunciation", "example": "example sentence"}`

#### Extract Text

- **URL**: `/extract_text/`
- **Method**: `POST`
- **Data Params**: `file=[multipart/form-data]`
- **Success Response**: `{"text": "Extracted text content from the file"}`

#### Extract Topic

- **URL**: `/extract_topic/`
- **Method**: `POST`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string], num_topics=Optional[int], num_words=Optional[int]`
- **Success Response**: `{"topic": ["word1", "word2", "word3"]}`

#### Summarize Text

- **URL**: `/summarize_text/`
- **Method**: `POST`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string], per=Optional[float]`
- **Success Response**: `{"summary": "Summarized text content"}`

#### Sentiment Analysis

- **URL**: `/sentiment_analysis/`
- **Method**: `POST`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string]`
- **Success Response**: `{"sentiment": "Positive"}`

#### Divide Into Paragraphs

- **URL**: `/divide_into_paragraphs/`
- **Method**: `POST`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string]`
- **Success Response**: `{"paragraphs": ["paragraph1", "paragraph2", "paragraph3"]}`

#### Tag Keywords

- **URL**: `/tag_keywords/`
- **Method**: `POST`
- **Data Params**: `file=Optional[multipart/form-data], text=Optional[string]`
- **Success Response**: `{"paragraph_keywords": {"paragraph1": ["word1", "word2"], "paragraph2": ["word3", "word4"], "paragraph3": ["word5", "word6"]}}`

#### Process File

- **URL**: `/process_file/`
- **Method**: `POST`
- **Data Params**: `file=[multipart/form-data]`
- **Success Response**: `{"topic": ["word1", "word2", "word3"], "summary": "Summarized text content", "paragraphs": [{"text": "paragraph1", "sentiment": "Positive", "keywords": {"word1": {"part_of_speech": "noun", "definition": "a word definition", "pronunciation": "pronunciation", "example": "example sentence"}, "word2": {...}}}, {"text": "paragraph2", "sentiment": "Neutral", "keywords": {...}}, {"text": "paragraph3", "sentiment": "Negative", "keywords": {...}}]}`


### Example Usage

Below is an example of how to use the text extraction endpoint. You can use a standard curl call:
```bash
curl -X POST "http://127.0.0.1:8000/extract_text/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/file.pdf"
```
Or use e.g. a request library in Python
```python
import requests

url = "http://localhost:8000/extract_text/"
file_path = "path/to/your/pdf_file.pdf"

with open(file_path, "rb") as f:
    files = {"file": (file_path, f)}
    response = requests.post(url, files=files)

print(response.json())
```
## Not Implemented Yet
- Google authentication and password recovery
- Document preview and analysis download
- Settings and Help tabs
