"""Flask app. Entry point from the web app."""
import random
import os
import requests
from flask import Flask, render_template, abort, request
import requests

from quote_engine import Ingestor
from meme_engine import MemeEngine

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # quote_files variable
    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    images = os.listdir(images_path)
    imgs = list(map(lambda x: images_path+x, images))

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']
    img = "tempimg.png"
    try:
        r = requests.get(url)
    except Exception:
        Exception("Unable to get image from the specified URL")
    with open(img, 'wb') as f:
        f.write(r.content)

    path = meme.make_meme(img, body, author)
    os.remove(img)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
