from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import tempfile
import shutil
import os
import json
import requests
import re
from PIL import Image
import pytesseract
from textblob import TextBlob
from PyPDF2 import PdfReader
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords
from collections import defaultdict
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import nltk
import eng_to_ipa as ipa
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict

nltk.download('wordnet')
nltk.download('cmudict')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')

app = FastAPI()

class ExtractTextResponse(BaseModel):
    text: str

class ExtractTopicResponse(BaseModel):
    topic: List[str]

class SummarizeTextResponse(BaseModel):
    summary: str

class ExtractDefinitionsResponse(BaseModel):
    part_of_speech: str
    definition: str
    pronunciation: str
    example: str


@app.post("/extract_text/", response_model=ExtractTextResponse)
async def extract_text(file: UploadFile = File(...)):

    allowed_extensions = ['pdf', 'jpg', 'png', 'doc', 'docx']
    max_file_size = 10 * 1024 * 1024  # 10 MB

    # Check the file extension
    extension = file.filename.split('.')[-1]
    if extension.lower() not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file format. Supported formats are PDF, JPG, PNG, DOC, and DOCX.")
    
    content = file.file.read()
    if len(content) > max_file_size:
        raise HTTPException(status_code=400, detail="File size exceeds the 10 MB limit.")

    text = ""
    if extension == 'pdf':
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(file.file.read())
            temp_file.flush()
            with open(temp_file.name, 'rb') as f:
                pdf_reader = PdfReader(f)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
    
    elif extension in ['png', 'jpg']:
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(file.file.read())
            temp_file.flush()
            img = Image.open(temp_file.name)
            text = pytesseract.image_to_string(img)

    elif extension in ['doc', 'docx']:
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(file.file.read())
            temp_file.flush()
            with open(temp_file.name, 'r') as f:
                text = f.read()
    
    return {"text": text}


@app.post("/extract_topic/", response_model=ExtractTopicResponse)
async def extract_topic(file: UploadFile = File(...), num_topics: Optional[int] = 1, num_words: Optional[int] = 3):

    try:
        text = await extract_text(file)
    except HTTPException as e:
        raise e

    text = text['text']
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() and word not in stop_words]
    
    # Filter words for nouns only
    tagged_words = nltk.pos_tag(words)
    nouns = [word for word, pos in tagged_words if pos in ('NN', 'NNS', 'NNP', 'NNPS')]
    
    dictionary = corpora.Dictionary([nouns])
    corpus = [dictionary.doc2bow([word]) for word in nouns]
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    topic_words = lda_model.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)

    topic = [word[0].capitalize() for word in topic_words[0][1]]

    return {"topic": topic}


@app.post("/summarize_text/", response_model=SummarizeTextResponse)
async def summarize_text(file: UploadFile = File(...), per: Optional[float] = 0.1):

    try:
        text = await extract_text(file)
    except HTTPException as e:
        raise e

    text = text['text']

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word] / max_frequency

    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens) * per)
    summary = nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary = [word.text for word in summary]

    return {"summary": ''.join(final_summary)}


@app.get("/extract_definitions/", response_model=ExtractDefinitionsResponse)
async def extract_definitions(word: str):

    def pos_to_human_readable(pos_tag):
        if pos_tag == 'n':
            return 'noun'
        elif pos_tag == 'v':
            return 'verb'
        elif pos_tag == 'a':
            return 'adjective'
        elif pos_tag == 's':
            return 'adjective satellite'
        elif pos_tag == 'r':
            return 'adverb'
        else:
            return 'unknown'

    def get_example_sentence(keyword, pos):

        from nltk.corpus import brown
        tagged_sentences = brown.tagged_sents(categories='news')

        for sent in tagged_sentences:
            for idx, (token, tag) in enumerate(sent):
                if token.lower() == keyword.lower() and pos_to_human_readable(tag[0].lower()) == pos:
                    return ' '.join([token for token, _ in sent])

        return 'No example available'

    synsets = wordnet.synsets(word)

    if synsets:
        definition = synsets[0].definition()
        pos = pos_to_human_readable(synsets[0].pos())
        pronunciation = ipa.convert(word)
        example = get_example_sentence(word, pos)

        return {
            'part_of_speech': pos,
            'definition': definition,
            'pronunciation': pronunciation,
            'example': example
        }

