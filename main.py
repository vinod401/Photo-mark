from tkinter.filedialog import askopenfilename
from PIL import Image
from text_watermark import TextMark


textmark = TextMark()

try:
    img_path = askopenfilename(initialdir="../Users/<name>/Pictures",
                                   title="Select A File", filetype=(("jpg", "*.jpg"), ("png", "*.png"))).strip()

except PermissionError:
    pass

else:
    image = Image.open(img_path)
    textmark.image_to_make(image=image)

    x = image.width - 200
    y = image.height - 75

    textmark.update_pos(x=x, y=y)
    textmark.make_watermark()
