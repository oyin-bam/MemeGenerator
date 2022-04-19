"""
The meme_engine module used the make_meme function to do the following.

Load a file from disk.
Transform image by resizing to a maximum width of.
500px while maintaining the input aspect ratio.
Add a caption to an image (string input) with a body.
and author to a random location on the image.
"""
from PIL import Image, ImageDraw, ImageFont
from random import randint
import os
import matplotlib.font_manager as fm
from math import ceil


class MemeEngine:
    """A MemeEngine use the make_meme method to create a meme from an image."""

    def __init__(self, output_dir):
        """Create and Instance of MemeEngine.

        The output directory supplied as the only arguments.
        :param output_dir: the directory to store a generated meme.
        """
        self.output_dir = output_dir

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Generate a meme from an image.

        :param img_path: path to the image the meme is generated from.
        :param text: quote to be written on the meme.
        :param author: author of the quote.
        :return The filepath of the generated meme.
        """ 
        img = Image.open(img_path)
        old_width, old_height = img.size
        height = ceil(old_height/old_width * width)
        new_img = img.resize((width, height))

        # add quote
        offset = 20
        text_pos = (randint(0, width/2), randint(0, height-60))
        author_pos = (text_pos[0], text_pos[1] + offset)

        draw = ImageDraw.Draw(new_img)
        # myfont = ImageFont.truetype('Tests/fonts/DejaVuSans.ttf')
        myfont = ImageFont.truetype(fm.findfont(
                                    fm.FontProperties('DejaVuSans.ttf')), 18)
        draw.text(text_pos, text, fill=(255, 255, 0), font=myfont)
        draw.text(author_pos, "- "+author, fill=(255, 255, 0), font=myfont)

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        filename = self.output_dir + "/" + img_path.split("/")[-1]
        new_img.save(filename)

        return filename
