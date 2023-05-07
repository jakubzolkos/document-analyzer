import os
import requests
import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile
from nlpapi import app

client = TestClient(app)

SAMPLE_PDF_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
SAMPLE_PDF_PATH = "dummy.pdf"

def download_sample_pdf():
    response = requests.get(SAMPLE_PDF_URL)
    with open(SAMPLE_PDF_PATH, "wb") as f:
        f.write(response.content)

def delete_sample_pdf():
    if os.path.exists(SAMPLE_PDF_PATH):
        os.remove(SAMPLE_PDF_PATH)

def test_extract_definitions():
    response = client.get("/extract_definitions/", params={"word": "computer"})
    assert response.status_code == 200
    assert "part_of_speech" in response.json()
    assert "definition" in response.json()
    assert "pronunciation" in response.json()
    assert "example" in response.json()

def test_extract_text_pdf():
    download_sample_pdf()
    with open(SAMPLE_PDF_PATH, "rb") as file:
        response = client.post("/extract_text/", files={"file": ("dummy.pdf", file, "application/pdf")})
    delete_sample_pdf()
    assert response.status_code == 200
    assert "text" in response.json()

def test_extract_text_invalid_file():
    response = client.post("/extract_text/", files={"file": ("invalid.txt", b"Invalid file", "text/plain")})
    assert response.status_code == 400
    assert "detail" in response.json()

def test_summarize_text_invalid_input():
    response = client.post("/summarize_text/", json={"text": ""})
    assert response.status_code == 400
    assert "detail" in response.json()
