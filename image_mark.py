from PIL import Image
default_image = Image.open("./images/default_watermark.png")
default_image = default_image.convert("RGBA")


class ImageMark:
    def __init__(self):
        self.base_image = None
        self.image_to_mark = default_image
        self.result_image = None
        self.x_pos = None
        self.y_pos = None

    def make_final_image(self):
        self.image_to_mark.thumbnail((500, 500))
        self.make_default_pos()

        new = Image.new("RGBA", self.base_image.size, (255, 255, 255, 0), )
        new.paste(self.image_to_mark, (self.x_pos, self.y_pos))
        self.result_image = Image.alpha_composite(self.base_image, new, )

    def make_default_pos(self):
        self.x_pos = self.base_image.width - self.image_to_mark.width - 20
        self.y_pos = self.base_image.height - self.image_to_mark.height - 20

    def receive_base_image(self, image):
        self.base_image = image

