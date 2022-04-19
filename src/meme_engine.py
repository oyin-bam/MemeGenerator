"""
The meme_engine module used the make_meme function to do the following.

Load a file from disk.
Transform image by resizing to a maximum width of.
500px while maintaining the input aspect ratio.
Add a caption to an image (string input) with a body.
and author to a random location on the image.
"""
from tkinter import font
from PIL import Image, ImageDraw, ImageFont
from random import randint
import os
import matplotlib.font_manager as fm
from math import ceil
from pathlib import Path
import textwrap

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

        # wrap text
        font_size = 18
        t = ceil(width/(font_size-3)) 
        text_list = textwrap.TextWrapper(t).wrap(text)
        author_list = textwrap.TextWrapper(t).wrap(author) 
        n = len(text_list)
        m = len(author_list)
        x_offset = max(len(text_list[0]), len(author_list[0])) * (font_size - 6)
        y_offset = (n + m) * font_size
        next_line_offset = font_size

        # get position
        text_pos = (randint(0, width-x_offset), randint(0, height-y_offset))
        author_pos = (text_pos[0], text_pos[1] + next_line_offset * n)

        draw = ImageDraw.Draw(new_img)
        myfont = ImageFont.truetype(fm.findfont(
                                    fm.FontProperties('DejaVuSans.ttf')), font_size)
        # draw body
        for i in range(n):
            pos = (text_pos[0], text_pos[1] + next_line_offset * i)
            draw.text(pos, text_list[i], fill=(255, 255, 0), font=myfont)

        # draw author
        for i in range(m):
            pos = (author_pos[0], author_pos[1] + next_line_offset * i)
            draw.text(pos, "- "+author_list[i], fill=(255, 255, 0), font=myfont)

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        filename = self.output_dir + "/" + Path(img_path).name
        new_img.save(filename)

        return filename

    
