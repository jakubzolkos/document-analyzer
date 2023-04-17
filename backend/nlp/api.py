import textract
from PIL import Image
import pytesseract
import re
import flair
from flair.data import Sentence
from flair.models import SequenceTagger
flair.device = "cpu"  # Use CPU instead of GPU to save resources


def extract_text(filename):

    file_extension = filename.split('.')[-1].lower()

    if file_extension == 'doc':
        text = textract.process(filename, method='antiword').decode('utf-8')
    elif file_extension == 'pdf':
        text = textract.process(filename, method='pdfminer').decode('utf-8')
    elif file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
        img = Image.open(filename)
        text = pytesseract.image_to_string(img)
    else:
        raise Exception('Unsupported file format')

    # Clean text
    text = re.sub(' +', ' ', text)
    text = text.strip()  
    text = re.sub(r'[^\w\s\.\'\",?!-]', '', text)
    text = re.sub(r'\n{3,}', '\n', text)

    return text


def divide_into_paragraphs(text):
    # Divide text into paragraphs
    return text.split('\n\n')


def extract_named_entities(text):
    # Load the NER model
    ner = SequenceTagger.load('ner')

    # Run the NER model on the input text
    sentence = flair.data.Sentence(text)
    ner.predict(sentence)

    # Extract the named entities and their types
    entities = []
    for entity in sentence.get_spans('ner'):
        entities.append((entity.text, entity.tag))

    return ' '.join([entity[0] for entity in entities if entity[1] in ["ORG", "PER", "LOC"]])

text = extract_text("/home/hyron/Desktop/UNI/CODING/bu/ec530/doc-analyzer/backend/media/jakub_zolkos_resume.pdf")
# paragraphs = divide_into_paragraphs(text)
# print(paragraphs)
ents = extract_named_entities(extract_named_entities(text))
print(ents)