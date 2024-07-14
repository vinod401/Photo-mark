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
        self.width = None
        self.height = None
        self.current_size = 5
        self.sizes = None
        self.processed_watermark = None

    def make_final_image(self):
        self.make_default_pos()

        new = Image.new("RGBA", self.base_image.size, (255, 255, 255, 0), )
        new.paste(self.processed_watermark, (self.x_pos, self.y_pos))
        self.result_image = Image.alpha_composite(self.base_image, new, )

    def make_default_pos(self):
        self.x_pos = self.base_image.width - self.processed_watermark.width - 20
        self.y_pos = self.base_image.height - self.processed_watermark.height - 20

    def update_size(self, size):
        self.current_size = size
        self.processed_watermark = self.image_to_mark.resize(self.sizes[size])

    def update_image_to_mark(self, image):
        self.image_to_mark = image

        self.update_info()
        # self.processed_watermark = self.image_to_mark.resize(self.sizes[5], resample=Image.Resampling.LANCZOS)

    def update_info(self):
        width = int((self.base_image.width*15)/100)
        height = int((self.base_image.height*15)/100)
        self.processed_watermark = self.image_to_mark.copy()

        self.processed_watermark.thumbnail((width, height))

        width = int(self.processed_watermark.width)
        height = int(self.processed_watermark.height)

        self.sizes = {
            5: (width, height),
            6: (width * 2, height * 2),
            7: (width * 3, height * 3),
            8: (width * 4, height * 4),
            9: (width * 5, height * 5),
            10: (width * 6, height * 6)
        }

    def receive_base_image(self, image):
        self.base_image = image
        self.update_info()





