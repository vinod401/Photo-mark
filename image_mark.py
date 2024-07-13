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
        self.processed_watermark = self.image_to_mark.resize(self.sizes[size])

    def update_image_to_mark(self, image):
        self.image_to_mark = image

        self.update_info()
        # self.processed_watermark = self.image_to_mark.resize(self.sizes[5], resample=Image.Resampling.LANCZOS)

    def update_info(self):
        width = int((self.base_image.width / 100))
        height = int((self.base_image.height / 100))
        self.processed_watermark = self.image_to_mark.copy()

        self.processed_watermark.thumbnail((width, height))

        width = int(self.processed_watermark.width)
        height = int(self.processed_watermark.height)

        self.sizes = {
            5: (width*10, height*10),
            6: (width * 20, height * 20),
            7: (width * 30, height * 30),
            8: (width * 40, height * 40),
            9: (width * 50, height * 50),
            10: (width * 100, height * 100)
        }

    def receive_base_image(self, image):
        self.base_image = image
        self.update_info()





