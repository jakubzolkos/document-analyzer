import json
import requests
import re
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup
from textblob import TextBlob
from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
from collections import defaultdict
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.utils import get_stop_words


class NLP:
    
    def __init__(self):

        self.text = ''
        self.summarized_text = ''
        self.paragraphs = []
        self.sentiments = []
        self.definitions = defaultdict(str)
        self.keywords = []

    def extract_text(self, file):
        
        extension = file.split('.')[-1]

        if extension == 'pdf':
            with open(file, 'rb') as f:
                pdf_reader = PdfReader(f)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    self.text += page.extract_text()
        
        elif extension in ['png', 'jpg']:
            img = Image.open(file)
            self.text = pytesseract.image_to_string(img)

        elif extension in ['doc', 'docx']:
            with open(file, 'r') as f:
                self.text = f.read()
        
        return self.text
            
    def clean_text(self):

        self.text = re.sub('\n', '', self.text)
        
    def summarize_text(self, text, ratio=0.05):

        language = 'english'
        sentence_count = max(1, int(ratio * len(sent_tokenize(text))))
        parser = PlaintextParser.from_string(text, Tokenizer(language))
        summarizer = LsaSummarizer()
        summarizer.stop_words = get_stop_words(language)
        summary = []
        for sentence in summarizer(parser.document, sentence_count):
            summary.append(str(sentence))

        self.summarized_text = '\n'.join(summary)
        
    def divide_into_paragraphs(self):
        self.paragraphs = sent_tokenize(self.summarized_text)
        
    def perform_sentiment_analysis(self):
        for paragraph in self.paragraphs:
            blob = TextBlob(paragraph)
            sentiment = blob.sentiment.polarity
            self.sentiments.append(sentiment)
            
    def extract_definitions(self):
        for word in word_tokenize(self.summarized_text):
            synsets = wordnet.synsets(word)
            if synsets:
                definition = synsets[0].definition()
                self.definitions[word] = definition
        
    def tag_keywords(self):
        for word in word_tokenize(self.summarized_text):
            synsets = wordnet.synsets(word)
            if synsets:
                self.keywords.append(word)
        
    def process_file(self, file_path):
        
        text = self.extract_text(file_path)
        self.clean_text()
        self.summarize_text(text)
        self.divide_into_paragraphs()
        self.perform_sentiment_analysis()
        self.extract_definitions()
        self.tag_keywords()
        
    def to_json(self, file_path=None):

        json_dict = {

            'text': self.text,
            'summarized_text': self.summarized_text,
            'paragraphs': self.paragraphs,
            'sentiments': self.sentiments,
            'definitions': self.definitions,
            'keywords': self.keywords
        }

        if file_path is not None:
            with open(file_path, 'w') as f:
                json.dump(json_dict, f)

        return json.dumps(json_dict)


nlp_tool = NLP()
nlp_tool.process_file('/home/hyron/Desktop/UNI/CODING/bu/ec530/doc-analyzer/backend/media/applsci-10-08660.pdf')
result_json = nlp_tool.to_json('output.json')
print(result_json)