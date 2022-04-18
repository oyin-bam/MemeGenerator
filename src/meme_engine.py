from PIL import Image, ImageDraw, ImageFont
from random import randint
import os
import matplotlib.font_manager as fm
from math import ceil

class MemeEngine:

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def make_meme(self, img_path, text, author, width=500) -> str:
        img = Image.open(img_path)
        old_width, old_height = img.size
        height = ceil(old_height/old_width * width)
        new_img = img.resize((width, height))

        #add quote
        offset = 20
        text_pos = (randint(0, width/2), randint(0, height-60))
        author_pos = (text_pos[0], text_pos[1] + offset)

        draw = ImageDraw.Draw(new_img)
        #myfont = ImageFont.truetype('Tests/fonts/DejaVuSans.ttf')
        myfont = ImageFont.truetype(fm.findfont(fm.FontProperties('DejaVuSans.ttf')),18)
        draw.text(text_pos, text, fill=(255,255,0), font=myfont)
        draw.text(author_pos, "- "+author, fill=(255,255,0), font=myfont)

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        filename = self.output_dir + "/" + img_path.split("/")[-1]
        new_img.save(filename)

        return filename


