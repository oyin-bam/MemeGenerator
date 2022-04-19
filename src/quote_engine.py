"""Provide various ingestors for ingesting different types of file."""

from signal import raise_signal
import tempfile
from typing import List
from abc import ABC, abstractmethod
from docx import Document
import pandas as pd
import subprocess
import os


class QuoteModel:
    """Model that encapsulates information about quote.

    it holds the body and author of the quote.
    """

    def __init__(self, body, author):
        """Create a new quote model with the quote and the author.

        :param body: quote.
        "paranm author: owner of the quote.
        """
        self.body = body
        self.author = author

    def __str__(self) -> str:
        """Return `str(self)`."""
        return f"{self.body} - {self.author}"


class IngestorInterface(ABC):
    """A general superclass for ingestors on different file types.

    The ingestor interface knows if a file can be ingested and.
    parse this file to generate all the quotes using the `QuoteModel`.
    """

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if a file can be imgested or not.

        Concrete subclasses must override this method
        to check the file type of interest.
        :param path: path to the quote file to be ingested.
        :return: whether the file can be ingested or not
        """
        pass

    @abstractmethod
    def parse(self, path: str) -> List[QuoteModel]:
        """Generate list of quotes with the `QuoteModel`.

        :param: path to the quote file to be processed.
        :return: list of `QuoteModels`.
        """
        pass


class Ingestor(IngestorInterface):
    """Encapsulates all the ingestors to provide one.

    Interface to load any supported file.
    Use the `parse` method to select the appropriate
    ingestor based on the file typr provided.
    """

    TEXTFILE = "txt"
    DOCXFILE = "docx"
    PDFFILE = "pdf"
    CSVFILE = "csv"

    def parse(path):
        """Select the appropriate ingestor based on the file type.

        :param: path to the file to be process.
        return: the result of the `parse` method of the selected ingestor.
        """
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
    """Ingestor for text file."""

    def parse(self, path):
        """Process a text file and get all quotes.

        :param: path to the text file to be processed.
        :return: list of `QuoteModels`
        """
        quotes = []
        with open(path, 'r') as f:
            for content in f.readlines():
                content = content.strip()
                if content:
                    body, author = content.split("-")
                    quotes.append(QuoteModel(body=body.strip(),
                                             author=author.strip()))
        return quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the file is a text file.

        :param path: path to the text file to be processed.
        :return: whether the file is a text file.
        """
        return path.split(".")[-1] == "txt"


class DocxIngestor(IngestorInterface):
    """Ingestor for docx file."""

    def parse(self, path: str):
        """Process a docx file and get all quotes.

        :param: path to the docx file to be processed.
        :return: list of `QuoteModels`
        """
        quotes = []
        doc = Document(path)
        for d in doc.paragraphs:
            content = d.text.strip()
            if content:
                body, author = content.split("-")
                quotes.append(QuoteModel(body=body.strip(),
                                         author=author.strip()))

        return quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the file is a docx file.

        :param path: path to the docx file to be processed.
        :return: whether the file is a docx file.
        """
        return path.split(".")[-1] == "docx"


class PDFIngestor(IngestorInterface):
    """Ingestor for pdf file."""

    def parse(self, path: str):
        """Process a pdf file and get all quotes.

        :param: path to the pdf file to be processed.
        :return: list of `QuoteModels`
        """
        quotes = []
        tempfile = "temp.txt"
        subprocess.run(['pdftotext', '-layout', path, tempfile],
                        stdout=subprocess.PIPE)

        try:
            tempfile = "temp.txt"
            subprocess.run(['pdftotext', '-layout', path, tempfile],
                           stdout=subprocess.PIPE)

            with open(tempfile, 'r') as f:
                for content in f.readlines():
                    content = content.strip()
                    if content:
                        body, author = content.split("-")
                        quotes.append(QuoteModel(body=body.strip(),
                                      author=author.strip()))
        except Exception:
            raise Exception("An Error occured while processing the pdf file")
        finally:
            os.remove(tempfile)

        return quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the file is a pdf file.

        :param path: path to the pdf file to be processed.
        :return: whether the file is a pdf file.
        """
        return path.split(".")[-1] == "pdf"


class CSVIngestor(IngestorInterface):
    """Ingestor for csv file."""

    def parse(self, path: str):
        """Process a csv file and get all quotes.

        :param: path to the csv file to be processed.
        :return: list of `QuoteModels`
        """
        quotes = []
        df = pd.read_csv(path)
        for _, rows in df.iterrows():
            body, author = rows['body'], rows['author']
            quotes.append(QuoteModel(body=body.strip(), author=author.strip()))

        return quotes

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the file is a csv file.

        :param path: path to the csv file to be processed.
        :return: whether the file is a csv file.
        """
        return path.split(".")[-1] == "csv"
