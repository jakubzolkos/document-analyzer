# Document Analyzer 
Written by Jakub Zolkos for EC 530: Software Engineering Principles 
## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Database](#database)


## Introduction
Document analyzer API that provides multiple text analysis features. Written using Django REST Framework.


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
