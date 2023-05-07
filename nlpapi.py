from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import tempfile
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
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gensim import corpora
from typing import List
from fastapi import Depends, HTTPException


nltk.download('wordnet')
nltk.download('cmudict')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')

app = FastAPI()


class DivideIntoParagraphsResponse(BaseModel):
    paragraphs: List[str]

class TagKeywordsResponse(BaseModel):
    paragraph_keywords: Dict[str, List[str]]

class ProcessFileResponse(BaseModel):
    topic: List[str]
    summary: str
    paragraphs: List[Dict]

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

class SentimentAnalysisResponse(BaseModel):
    sentiment: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str


@app.get("/extract_definitions/", response_model=ExtractDefinitionsResponse)
async def extract_definitions(word: str):

    if word is None:
        raise HTTPException(status_code=400, detail="No input")

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

    try:
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
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not obtain word definition")


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

    try:
        with tempfile.NamedTemporaryFile() as temp_file:

            temp_file.write(content)
            temp_file.flush()

            if extension == 'pdf':

                with open(temp_file.name, 'rb') as f:
                    pdf_reader = PdfReader(f)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()
            
            elif extension in ['png', 'jpg']:

                img = Image.open(temp_file.name)
                text = pytesseract.image_to_string(img)

            elif extension in ['doc', 'docx']:
    
                with open(temp_file.name, 'r') as f:
                    text = f.read()
        
        return {"text": text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
        

@app.post("/extract_topic/", response_model=ExtractTopicResponse)
async def extract_topic(file: Optional[UploadFile] = File(None), text: Optional[str] = None, num_topics: Optional[int] = 1, num_words: Optional[int] = 3):
    
    if not file and not text:
        raise HTTPException(status_code=400, detail="Please provide either a file or text")
    
    if file and text:
        raise HTTPException(status_code=400, detail="Can't process both file and text at the same time")
    
    if file and not text:
        try:
            text = await extract_text(file)
        except HTTPException as e:
            raise e

        text = text['text']


    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
        
    # Filter words for nouns and adjectives only
    tagged_words = nltk.pos_tag(words)
    valid_tags = ('NN', 'NNS', 'JJ', 'JJR', 'JJS')
    words = [word.lower() for word, pos in tagged_words if word.isalnum() and pos in valid_tags and word not in stop_words]
    
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Create a dictionary and a corpus
    dictionary = corpora.Dictionary([words])
    corpus = [dictionary.doc2bow([word]) for word in words]
    
    # Train an LDA model and extract topic words
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    topic_words = lda_model.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)

    topic = [word[0].capitalize() for word in topic_words[0][1]]

    return {"topic": topic}


@app.post("/summarize_text/", response_model=SummarizeTextResponse)
async def summarize_text(file: Optional[UploadFile] = File(None), text: Optional[str] = None, per: Optional[float] = 0.1):
    
    if not file and not text:
        raise HTTPException(status_code=400, detail="Please provide either a file or text")
    
    if file and text:
        raise HTTPException(status_code=400, detail="Can't process both file and text at the same time")
    
    if file and not text:
        try:
            text = await extract_text(file)
        except HTTPException as e:
            raise e

        text = text['text']

    if not text:
        raise HTTPException(status_code=400, detail="Please provide either a file or text")

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


@app.post("/sentiment_analysis/", response_model=SentimentAnalysisResponse)
async def sentiment_analysis(file: Optional[UploadFile] = File(None), text: Optional[str] = None):

    if not file and not text:
        raise HTTPException(status_code=400, detail="Please provide either a file or text")
    
    if file and text:
        raise HTTPException(status_code=400, detail="Can't process both file and text at the same time")
    
    if file and not text:
        try:
            text = await extract_text(file)
        except HTTPException as e:
            raise e

        text = text['text']

    def get_sentiment_description(score):
        if score >= 0.5:
            return "Very Positive"
        elif score > 0.1:
            return "Positive"
        elif score > -0.1:
            return "Neutral"
        elif score > -0.5:
            return "Negative"
        else:
            return "Very Negative"

    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    sentiment = get_sentiment_description(sentiment_score)

    return {"sentiment": sentiment}


@app.post("/divide_into_paragraphs/", response_model=DivideIntoParagraphsResponse)
async def divide_into_paragraphs(file: Optional[UploadFile] = File(None), text: Optional[str] = None):

    if not file and not text:
        raise HTTPException(status_code=400, detail="Please provide either a file or text")
    
    if file and text:
        raise HTTPException(status_code=400, detail="Can't process both file and text at the same time")
    
    if file and not text:
        try:
            text = await extract_text(file)
        except HTTPException as e:
            raise e

        text = text['text']

    paragraphs = re.split('\n\n|\n\t|\n', text)
    return {"paragraphs": paragraphs}


@app.post("/tag_keywords/", response_model=TagKeywordsResponse)
async def tag_keywords(file: Optional[UploadFile] = File(None), text: Optional[List[str]] = None):

    if not file and not text:
        raise HTTPException(status_code=400, detail="Please provide either a file or text")
    
    if file and text:
        raise HTTPException(status_code=400, detail="Can't process both file and text at the same time")
    
    if file and not text:
        try:
            text = await extract_text(file)
        except HTTPException as e:
            raise e

        text = text['text']
        text = re.split('\n\n|\n\t|\n', text)

    def is_number_string(s):
        return s.replace('.', '', 1).isdigit()

    def get_keywords(paragraph, num_keywords):
        try:
            stop_words = list(set(stopwords.words("english")))
            vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=r'(?u)\b[A-Za-z]+\b')
            tfidf_matrix = vectorizer.fit_transform([paragraph])
            feature_names = vectorizer.get_feature_names_out()
            importance = tfidf_matrix.toarray()[0]

            # Use a heap to store the top N keywords
            top_keywords = []

            import heapq
            for index, value in enumerate(importance):
                word = feature_names[index]
                if not is_number_string(word):
                    if len(top_keywords) < num_keywords:
                        heapq.heappush(top_keywords, (value, word))
                    else:
                        heapq.heappushpop(top_keywords, (value, word))

            # Extract keywords from the heap
            return [word for _, word in sorted(top_keywords, reverse=True)]

        except ValueError:
            return []

    paragraph_keywords = {}
    for paragraph in text:
        paragraph_length = len(word_tokenize(paragraph))
        num_keywords = min(max(paragraph_length // 10, 2), 5)
        keywords = get_keywords(paragraph, num_keywords)
        paragraph_keywords[paragraph] = keywords

    return {"paragraph_keywords": paragraph_keywords}


@app.post("/process_file/", response_model=ProcessFileResponse)
async def process_file(file: UploadFile = File(...)):

    text = (await extract_text(file))["text"]
    summary = (await summarize_text(file=None, text=text))["summary"]
    topic = (await extract_topic(file=None, text=text))["topic"]

    paragraphs = re.split('\n\n|\n\t|\n', text)

    # Perform sentiment analysis
    sentiments = []
    for paragraph in paragraphs:
        sentiment_response = await sentiment_analysis(file=None, text=paragraph)
        sentiments.append(sentiment_response["sentiment"])

    # Tag keywords
    paragraph_keywords = await tag_keywords(file=None, text=paragraphs)
 
    # Prepare the final response
    result = {
        "topic": topic,
        "summary": summary,
        "paragraphs": [{"text": p, "sentiment": s, "keywords": k} for p, s, k in zip(paragraphs, sentiments, paragraph_keywords["paragraph_keywords"].values())]
    }

    for element in result["paragraphs"]:
        keys = {keyword: await extract_definitions(keyword) for keyword in element["keywords"]}
        element["keywords"] = keys

    return result