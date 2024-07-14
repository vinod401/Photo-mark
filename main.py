from tkinter import *
from tkinter import ttk, colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
from text_watermark import TextMark
from image_mark import ImageMark
import subprocess

BASE_IMAGE = None
DISPLAY_IMAGE = None
MAX_SIZE = (720, 560)
textmark = TextMark()
image_mark = ImageMark()

# ---------------------------------------------text_water_mark--------------------------------------------------------
def textmark_active():
    # disabling image watermark option
    image_browse_btn.config(state="disabled")

    # enabling text watermark options
    text_box.config(state="normal")
    fonts.config(state="readonly")
    color_box.configure(state="normal")
    text_size.config(state="normal")

    rotation.set(textmark.rotation)
    text_size.delete(0, END)
    text_size.insert(1, textmark.size)

    textmark.image_to_make(image=BASE_IMAGE)
    textmark.make_final_image()
    display_result()


def update_text_size():
    size = int(text_size.get())
    # if text_size.get().isdigit():
    #     size = int(text_size.get())
    # elif text_size.get() == "":
    #     size = textmark.size
    # else:
    #     text_size.delete(first=0, last=END)
    #     text_size.insert(index=0, string="40")
    #     size = int(text_size.get())
    if radio_value.get() == "text":
        textmark.size = size
        textmark.default_pos()
        textmark_active()
    else:
        image_mark.update_size(size=size)

        image_mark_active()


def update_textbox(event):
    textmark.text = text_box.get()
    textmark_active()


def update_text_color():
    color_code = colorchooser.askcolor(title="Choose color")
    color_box.config(background=str(color_code[1]))
    textmark.color = color_code[0]
    textmark_active()


def text_font_update(event):
    textmark.font = current_font.get()
    textmark_active()
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------image_water_mark--------------------------------------------------------


def image_mark_active():
    # disabling text watermark options
    fonts.config(state="disabled")
    text_box.config(state="disabled")
    color_box.configure(state="disabled")
    # text_size.config(state="disabled")

    # enabling image water mark option
    image_browse_btn.config(state="normal")
    text_size.delete(0, END)
    text_size.insert(1, image_mark.current_size)

    image_mark.make_final_image()
    display_result()


def image_browse():

    # saving the file path of the image to be watermarked only jpeg or png can be selected
    filetype = (("JPG files", "*.jpg",), ("JPEG files", "*.jpeg",), ("PNG files", "*.png",))
    img_path = askopenfilename(initialdir="../Users/<name>/Pictures",
                               title="Select A File", filetypes=filetype)
    if img_path:
        water_mark_image = Image.open(img_path)
        water_mark_image = water_mark_image.convert("RGBA")
        image_mark.update_image_to_mark(image=water_mark_image)
        image_mark_active()

# ----------------------------------------------------------------------------------------------------------------------


def update_rotation():
    if radio_value.get() == "text":
        textmark.rotation = int(rotation.get())
        textmark_active()


def update_opacity(new_value):

    opacity_label.config(text=f"{int(opacity.get())}%")

    if radio_value.get() == "text":
        textmark.opacity = int((255 * opacity.get() / 100))
        textmark_active()


def display_result():
    global DISPLAY_IMAGE

    if radio_value.get() == "text":
        DISPLAY_IMAGE = textmark.result_image
    else:
        DISPLAY_IMAGE = image_mark.result_image

    DISPLAY_IMAGE.thumbnail(MAX_SIZE)
    DISPLAY_IMAGE = ImageTk.PhotoImage(DISPLAY_IMAGE)

    canvas.config(width=720, height=560)
    canvas.create_image(360, 280, image=DISPLAY_IMAGE)
    canvas.image = DISPLAY_IMAGE


def upload_image():
    global BASE_IMAGE
    # saving the file path of the image to be watermarked only jpeg or png can be selected
    filetype = (("JPG files", "*.jpg",), ("JPEG files", "*.jpeg",), ("PNG files", "*.png",))
    img_path = askopenfilename(initialdir="../Users/<name>/Pictures",
                               title="Select A File", filetypes=filetype)
    if img_path:
        text_radio_btn.config(state="normal")
        image_radio_btn.config(state="normal")
        opacity.config(state="normal")
        rotation.config(state="readonly")
        text_size.config(state="readonly")
        move_up_btn.config(state="normal")
        move_down_btn.config(state="normal")
        move_left_btn.config(state="normal")
        move_right_btn.config(state="normal")
        reset_pos_btn.config(state="normal")
        save_btn.config(state="normal")

        #  every time a new photo is uploaded by default it applies the text watermark
        BASE_IMAGE = Image.open(img_path)
        BASE_IMAGE = BASE_IMAGE.convert("RGBA")

        textmark.image_to_make(image=BASE_IMAGE)
        image_mark.receive_base_image(image=BASE_IMAGE)

        radio_value.set("text")
        opacity.set(75)

        textmark.default_pos()
        textmark_active()


def move_up():
    if radio_value.get() == "text":
        textmark.move_up()
    else:
        pass
    display_result()


def move_down():
    if radio_value.get() == "text":
        textmark.move_down()
    else:
        pass
    display_result()


def move_left():
    if radio_value.get() == "text":
        textmark.move_left()
    else:
        pass
    display_result()


def move_right():
    if radio_value.get() == "text":
        textmark.move_right()
    else:
        pass
    display_result()


def default_position():
    rotation.set(0)
    if radio_value.get() == "text":
        textmark.default_pos()
        textmark_active()
    else:
        pass


def save_image():

    # save image as a new file
    filetype = [("PNG files", ".png",), ("JPG files", ".jpg",), ("JPEG files", ".jpeg",)]
    path = asksaveasfilename(confirmoverwrite=True, defaultextension="png",
                             filetypes=filetype, title="Photmark", initialfile="Photomark_image")
    if path:
        if radio_value.get() == "text":
            textmark.result_image.save(path)
        else:
            image_mark.result_image.save(path)


root = Tk()

upload_button = ttk.Button(root, text="Upload", command=upload_image)
upload_button.pack()

radio_value = StringVar(value="text")

# ----------------------------------------------text watermark -----------------------------------------------------
text_radio_btn = ttk.Radiobutton(root, text="Text Water Mark", value="text", variable=radio_value, state="disabled",
                                 command=textmark_active)
text_radio_btn.pack()
text_box = ttk.Entry(root)
text_box.pack()
text_box.bind("<KeyRelease>", update_textbox)
text_box.insert(index=1, string=textmark.text)
text_box.config(state="disabled")

current_font = StringVar()
fonts = ttk.Combobox(root, width=10, state="readonly", textvariable=current_font)
fonts["values"] = textmark.font_list
fonts.bind("<<ComboboxSelected>>", text_font_update)
fonts.pack()
fonts.current(2)
fonts.config(state="disabled")

color_box = Button(root, width=5, borderwidth=0, background="white", state="disabled", command=update_text_color)
color_box.pack()

# text_size = Entry(width=5,)
# text_size.pack()
# text_size.insert(index=0, string=textmark.size)
# text_size.bind("<KeyRelease>", update_text_size)
# text_size.config(state="disabled")

text_size = Spinbox(from_=5, to=10, command=update_text_size, wrap=True, state="disabled")
text_size.pack()
# text_size.config(state="disabled")

# --------------------------------------------------------------------------------------------------------------------

# -------------------------------------image watermark --------------------------------------------------------------
image_radio_btn = ttk.Radiobutton(root, text="Image Water Mark", value="image", variable=radio_value, state="disabled",
                                  command=image_mark_active,)
image_radio_btn.pack()

image_browse_btn = Button(root, text="Browse", command=image_browse, state="disabled")
image_browse_btn.pack()

# -------------------------------------------------------------------------------------------------------------------

# ----------------------------------------common options----------------------------------------------------------

opacity = ttk.Scale(root, from_=0, to=100, command=update_opacity, state="disabled", value=75)
opacity.pack()

opacity_label = ttk.Label(root, text=f"{opacity.get()}")
opacity_label.pack()

rotation = ttk.Spinbox(width=5, from_=0, to=360, increment=30, command=update_rotation, wrap=True, state="readonly",)
rotation.set(0)
rotation.config(state="disabled")
rotation.pack()

# edit position button
move_up_btn = Button(text="up", command=move_up, state="disabled")
move_up_btn.pack()

move_down_btn = Button(text="down", command=move_down, state="disabled")

move_down_btn.pack()

move_left_btn = Button(text="left", command=move_left, state="disabled")
move_left_btn.pack()

move_right_btn = Button(text="right", command=move_right, state="disabled")
move_right_btn.pack()

reset_pos_btn = Button(text="reset", command=default_position, state="disabled")
reset_pos_btn.pack()

save_btn = Button(text="save", command=save_image, state="disabled")
save_btn.pack()
# ----------------------------------------------------------------------------------------------------------------


canvas = Canvas(root, width=0, height=0)
canvas.pack()

root.mainloop()
