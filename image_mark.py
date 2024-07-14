from PIL import Image
default_image = Image.open("./images/default_watermark.png")
default_image = default_image.convert("RGBA")


class ImageMark:
    def __init__(self):
        self.opacity = 191
        self.base_image = None
        self.image_to_mark = default_image
        self.result_image = None
        self.x_pos = None
        self.y_pos = None
        self.width = None
        self.height = None
        self.current_size = 5
        self.sizes = None
        self.rotation = 0
        self.size_adjusted_water_mark = None
        self.opacity_adjusted_water_mark = None
        self.water_mark_width = None
        self.water_mark_height = None

    def make_final_image(self):

        rotated_image = self.opacity_adjusted_water_mark.rotate(angle=self.rotation, expand=True, )
        self.height = rotated_image.height
        self.width = rotated_image.width
        new = Image.new("RGBA", self.base_image.size, (255, 255, 255, 0), )
        new.paste(rotated_image, (self.x_pos, self.y_pos))
        self.result_image = Image.alpha_composite(self.base_image, new, )

    def update_opacity(self):
        new_data = []
        self.opacity_adjusted_water_mark = self.size_adjusted_water_mark.copy()
        image_data = self.size_adjusted_water_mark.getdata()

        for item in image_data:
            if item[3] > self.opacity:
                new_data.append((item[0], item[1], item[2], self.opacity))
            else:
                new_data.append(item)
        self.opacity_adjusted_water_mark.putdata(new_data)

    def make_default_pos(self):
        self.x_pos = self.base_image.width - self.width - 20
        self.y_pos = self.base_image.height - self.height - 20

    def update_size(self, size):
        self.current_size = size
        self.size_adjusted_water_mark = self.image_to_mark.resize(self.sizes[size])
        self.update_opacity()
        # self.opacity_adjusted_water_mark = self.size_processed_water_mark.copy()

    def update_image_to_mark(self, image):
        self.image_to_mark = image

        self.update_info()
        # self.processed_watermark = self.image_to_mark.resize(self.sizes[5], resample=Image.Resampling.LANCZOS)

    def update_info(self):
        self.current_size = 5
        self.rotation = 0
        self.width = int((self.base_image.width*15)/100)
        self.height = int((self.base_image.height*15)/100)
        self.size_adjusted_water_mark = self.image_to_mark.copy()

        self.size_adjusted_water_mark.thumbnail((self.width, self.height))
        self.opacity_adjusted_water_mark = self.size_adjusted_water_mark.copy()

        self.width = int(self.size_adjusted_water_mark.width)
        self.height = int(self.size_adjusted_water_mark.height)

        self.sizes = {
            5: (self.width, self.height),
            6: (self.width * 2, self.height * 2),
            7: (self.width * 3, self.height * 3),
            8: (self.width * 4, self.height * 4),
            9: (self.width * 5, self.height * 5),
            10: (self.width * 6, self.height * 6)
        }
        self.make_default_pos()

    def move_up(self):
        self.y_pos = self.y_pos - 20
        self.make_final_image()

    def move_down(self):
        self.y_pos = self.y_pos + 20
        self.make_final_image()

    def move_left(self):
        self.x_pos = self.x_pos - 20
        self.make_final_image()

    def move_right(self):
        self.x_pos = self.x_pos + 20
        self.make_final_image()

    def receive_base_image(self, image):
        self.base_image = image
        self.update_info()

    def put_default_mark(self):
        self.image_to_mark = default_image
        self.update_info()




