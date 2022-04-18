import tempfile
from typing import List
from abc import ABC, abstractmethod
from docx import Document
import pandas as pd
import subprocess
import os

class QuoteModel:

    def __init__(self, body, author):
        self.body = body
        self.author = author

    def __str__(self) -> str:
        return f"{self.body} - {self.author}"


class IngestorInterface(ABC):

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        pass

    @abstractmethod
    def parse(self, path: str) -> List[QuoteModel]:
        pass


class Ingestor(IngestorInterface):
    TEXTFILE = "txt"
    DOCXFILE = "docx"
    PDFFILE = "pdf"
    CSVFILE = "csv"

    def parse(path):  
        if TextIngestor.can_ingest(path):
            ingestor = TextIngestor()
        elif DocxIngestor.can_ingest(path):
            ingestor = DocxIngestor()
        elif PDFIngestor.can_ingest(path):
            ingestor = PDFIngestor()
        elif CSVIngestor.can_ingest(path):
            ingestor = CSVIngestor()
        else:
            return []

        return ingestor.parse(path)


class TextIngestor(IngestorInterface):

    def parse(self, path):
        quotes = []
        with open(path, 'r') as f:
            for content in f.readlines():
                if content:
                    body, author = content.split("-")
                    quotes.append(QuoteModel(body=body.strip(), author=author.strip()))

        return quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.split(".")[-1] == "txt"

class DocxIngestor(IngestorInterface):

    def parse(self, path: str):
        quotes = []
        doc = Document(path)
        for d in doc.paragraphs:
            content = d.text
            if content:
                body, author = content.split("-")
                quotes.append(QuoteModel(body=body.strip(), author=author.strip()))

        return quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.split(".")[-1] == "docx"

class PDFIngestor(IngestorInterface):

    def parse(self, path: str):
        quotes = []
        try:
            #TODO modify this line to extract relative path
            tempfile = "." + path.split(".")[1] + ".txt"
            subprocess.run(['pdftotext', '-layout', path, tempfile], stdout=subprocess.PIPE)

            with open(tempfile, 'r') as f:
                for content in f.readlines():
                    if content:
                        body, author = content.split("-")
                        quotes.append(QuoteModel(body=body.strip(), author=author.strip()))
        except:
            pass
        finally:
            os.remove(tempfile)
        
        return quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.split(".")[-1] == "pdf"

class CSVIngestor(IngestorInterface):

    def parse(self, path: str):
        quotes = []
        df = pd.read_csv(path)
        for _,rows in df.iterrows():
            body, author = rows['body'], rows['author']
            quotes.append(QuoteModel(body=body.strip(), author=author.strip()))

        return quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.split(".")[-1] == "csv"
