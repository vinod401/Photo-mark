from PIL import ImageFont
from PIL import ImageDraw, Image
import matplotlib.font_manager as fm


class TextMark:
    def __init__(self):
        self.font_list = sorted(set([f.name for f in fm.fontManager.ttflist]))
        self.text = "PHOTOMARK"
        self.font = "arial"
        self.opacity = 255
        self.size = 5
        self.color = (255, 255, 255)
        self.color_with_opacity = (self.color + (self.opacity, ))
        self.text_width = None
        self.text_height = None
        self.x_pos = 0
        self.y_pos = 0
        self.rotation = 0

        self.image = None
        self.rotated_image = None
        self.result_image = None

    def make_water_mark(self):
        # the size is relative to the image size
        relative_size = int((self.size*self.image.width)/100)
        try:
            font = ImageFont.truetype(fm.findfont(fm.FontProperties(family=self.font, style=None)), relative_size)
        except ValueError:
            pass

        else:
            self.color_with_opacity = (self.color + (self.opacity,))
            # determining the size of the text in the give font and size
            self.text_width = font.getbbox(self.text)[2]
            self.text_height = font.getbbox(self.text)[3]

            # creating a blank transparent image in the size of the text
            blank_transparent_image = Image.new("RGBA", (self.text_width, self.text_height), (255, 255, 255, 0))

            # drawing the text in the blank image created
            draw = ImageDraw.Draw(mode="RGBA", im=blank_transparent_image)
            draw.text((0, 0), text=self.text, fill=self.color_with_opacity, font=font, )

            # applying the rotation if any by default is zero
            # the expand parameter is to avoid cropping of text while rotating
            self.rotated_image = blank_transparent_image.rotate(angle=self.rotation, expand=True)
            self.text_width = self.rotated_image.width
            self.text_height = self.rotated_image.height


    def make_final_image(self):
        """makes the text watermark given in the photo"""

        self.result_image = self.image.copy()
        self.result_image = self.result_image.convert("RGBA")

        new = Image.new("RGBA", self.result_image.size, (255, 255, 255, 0),)
        new.paste(self.rotated_image, (self.x_pos, self.y_pos))
        self.result_image = Image.alpha_composite(self.result_image, new, )

    def default_pos(self):

        self.make_water_mark()
        width = self.image.width
        height = self.image.height
        self.x_pos = width - self.text_width - 20
        self.y_pos = height - self.text_height - 20

        # self.make_water_mark()

    def move_up(self):
        self.y_pos = self.y_pos - 20
        self.make_water_mark()
        self.make_final_image()

    def move_down(self):
        self.y_pos = self.y_pos + 20
        self.make_water_mark()
        self.make_final_image()

    def move_left(self):
        self.x_pos = self.x_pos - 20
        self.make_water_mark()
        self.make_final_image()

    def move_right(self):
        self.x_pos = self.x_pos + 20
        self.make_water_mark()
        self.make_final_image()

    def image_to_make(self, image):
        """receives an image to make the watermark"""
        self.image = image
        self.make_water_mark()

