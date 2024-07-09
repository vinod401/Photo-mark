from PIL import ImageFont
from PIL import ImageDraw, Image


class TextMark:
    def __init__(self):
        self.text = "PHOTOMARK"
        self.font = "arial"
        self.size = 40
        self.color = "#ffffff"
        self.x_pos = 0
        self.y_pos = 0
        self.image = None
        self.result_image = None

    def make_watermark(self):
        self.result_image = self.image.copy()
        font = ImageFont.truetype(self.font, self.size)
        draw = ImageDraw.Draw(self.result_image)
        draw.text((self.x_pos, self.y_pos), self.text, self.color, font=font, anchor='ms')
        self.result_image.show()


    def update_pos(self, x, y):

        self.x_pos = x
        self.y_pos = y



    def image_to_make(self, image):
        self.image = image




