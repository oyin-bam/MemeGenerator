"""Entry point from the command line."""
import imp
import os
import random
import argparse
from quote_engine import Ingestor
from quote_engine import QuoteModel
from meme_engine import MemeEngine


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote.

    :param path: path to save the generated meme.
    :param body: the quote to be written on the meme.
    :param author: the author of the quote.
    :returns The path the generated meme is saved.
    """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       '..',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser(description="Generate a meme")
    parser.add_argument('--path', type=str, help='The path of the image')
    parser.add_argument('--body', type=str, 
                        help='The quote to be added to the meme')
    parser.add_argument('--author', type=str, help='The author of the quote')
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
