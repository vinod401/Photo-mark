from tkinter import *
from tkinter import ttk, font, colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
from text_watermark import TextMark

BASE_IMAGE = None
DISPLAY_IMAGE = None
MAX_SIZE = (720, 560)
textmark = TextMark()


def update_textbox(event):
    textmark.text = text_box.get()
    textmark_active()

def update_color():
    color_code = colorchooser.askcolor(title="Choose color")
    color_box.config(background=color_code[1])
    textmark.color = color_code[0]
    textmark_active()

def textmark_active():
    global DISPLAY_IMAGE, BASE_IMAGE
    text_box.config(state="normal")
    fonts.config(state="readonly")
    color_box.configure(state="normal")

    textmark.image_to_make(image=BASE_IMAGE)
    textmark.default_pos()
    DISPLAY_IMAGE = textmark.result_image
    DISPLAY_IMAGE.thumbnail(MAX_SIZE)
    DISPLAY_IMAGE = ImageTk.PhotoImage(DISPLAY_IMAGE)

    canvas.config(width=720, height=560)
    canvas.create_image(360, 280, image=DISPLAY_IMAGE)
    canvas.image = DISPLAY_IMAGE


def font_changed(event):
    textmark.font = current_font.get()
    textmark_active()


def image_mark_active():
    fonts.config(state="disabled")
    text_box.config(state="disabled")
    color_box.configure(state="disabled")


def upload_image():
    global BASE_IMAGE
    # saving the file path of the image to be watermarked only jpeg or png can be selected

    img_path = askopenfilename(initialdir="../Users/<name>/Pictures",
                               title="Select A File", filetype=(("jpg", "*.jpg"), ("png", "*.png"))).strip()
    if img_path:
        BASE_IMAGE = Image.open(img_path)

        text_radio_btn.config(state="normal")
        image_radio_btn.config(state="normal")
        textmark_active()


def create_text_mark():
    # saving the file path of the image to be watermarked only jpeg or png can be selected

    img_path = askopenfilename(initialdir="../Users/<name>/Pictures",
                               title="Select A File", filetype=(("jpg", "*.jpg"), ("png", "*.png"))).strip()
    if img_path:
        image = Image.open(img_path)

        textmark.image_to_make(image=image)
        textmark.default_pos()

        # making text mark
        # textmark.make_watermark()
        textmark.result_image.show()
    else:
        pass


def save_image():
    # save image as a new file
    path = asksaveasfilename(confirmoverwrite=True, defaultextension="png",
                             filetypes=[("png", ".png"), ("jpeg", ".jpg")])
    if path:
        textmark.result_image.save(path)


root = Tk()

upload_button = ttk.Button(text="Upload", command=upload_image)
upload_button.pack()

radio_value = StringVar(value="text")

# ----------------------------------------------text watermark -----------------------------------------------------
text_radio_btn = ttk.Radiobutton(root, text="Text Water Mark", value="text", variable=radio_value, state="disabled",
                                 command=textmark_active)
text_radio_btn.pack()
text_box = ttk.Entry()
text_box.pack()
text_box.bind("<KeyRelease>", update_textbox)
text_box.insert(index=1, string=textmark.text)
text_box.config(state="disabled")

current_font = StringVar()
fonts = ttk.Combobox(root, width=10, state="readonly", textvariable=current_font)
fonts["values"] = textmark.font_list
fonts.bind("<<ComboboxSelected>>", font_changed)
fonts.pack()
fonts.current(2)
fonts.config(state="disabled")

color_box = Button(width=5, borderwidth=0, background="white", state="disabled", command=update_color)
color_box.pack()

# --------------------------------------------------------------------------------------------------------------------

# -------------------------------------image watermark --------------------------------------------------------------
image_radio_btn = ttk.Radiobutton(root, text="Image Water Mark", value="image", variable=radio_value, state="disabled",
                                  command=image_mark_active)
image_radio_btn.pack()

# -------------------------------------------------------------------------------------------------------------------

canvas = Canvas(root, width=0, height=0)
canvas.pack()


root.mainloop()
