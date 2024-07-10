from tkinter import *
from tkinter import ttk, colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
from text_watermark import TextMark
import subprocess

BASE_IMAGE = None
DISPLAY_IMAGE = None
MAX_SIZE = (720, 560)
textmark = TextMark()


def textmark_active():

    text_box.config(state="normal")
    fonts.config(state="readonly")
    color_box.configure(state="normal")
    text_size.config(state="normal")

    textmark.image_to_make(image=BASE_IMAGE)
    textmark.make_final_image()
    display_result()


def update_text_size(event):

    if text_size.get().isdigit():
        size = int(text_size.get())
    elif text_size.get() == "":
        size = textmark.size
    else:
        text_size.delete(first=0, last=END)
        text_size.insert(index=0, string="40")
        size = int(text_size.get())

    textmark.size = size
    textmark_active()


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


def image_mark_active():
    fonts.config(state="disabled")
    text_box.config(state="disabled")
    color_box.configure(state="disabled")
    text_size.config(state="disabled")


def update_rotation():
    rotation_angle = int(rotation.get())

    textmark.rotation = rotation_angle
    textmark_active()


def update_opacity(new_value):

    opacity_percentage = int(opacity.get())
    opacity_label.config(text=f"{opacity_percentage}%")

    if radio_value.get() == "text":
        textmark.opacity = int((255 * opacity_percentage) / 100)
        textmark_active()


def display_result():
    global DISPLAY_IMAGE, BASE_IMAGE
    DISPLAY_IMAGE = textmark.result_image
    DISPLAY_IMAGE.thumbnail(MAX_SIZE)
    DISPLAY_IMAGE = ImageTk.PhotoImage(DISPLAY_IMAGE)

    canvas.config(width=720, height=560)
    canvas.create_image(360, 280, image=DISPLAY_IMAGE)
    canvas.image = DISPLAY_IMAGE


def upload_image():
    global BASE_IMAGE
    # saving the file path of the image to be watermarked only jpeg or png can be selected

    img_path = askopenfilename(initialdir="../Users/<name>/Pictures",
                               title="Select A File", filetype=(("jpg", "*.jpg"), ("png", "*.png"))).strip()
    if img_path:
        text_radio_btn.config(state="normal")
        image_radio_btn.config(state="normal")
        opacity.config(state="normal")
        rotation.config(state="readonly")
        text_size.config(state="normal")
        move_up_btn.config(state="normal")
        move_down_btn.config(state="normal")
        move_left_btn.config(state="normal")
        move_right_btn.config(state="normal")
        reset_pos_btn.config(state="normal")
        save_btn.config(state="normal")

        BASE_IMAGE = Image.open(img_path)
        textmark.image_to_make(image=BASE_IMAGE)
        textmark.default_pos()
        opacity.set(75)
        textmark_active()


def move_up():
    textmark.move_up()
    display_result()


def move_down():
    textmark.move_down()
    display_result()


def move_left():
    textmark.move_left()
    display_result()


def move_right():
    textmark.move_right()
    display_result()


def default_position():
    textmark.default_pos()
    textmark_active()


def save_image():

    # save image as a new file
    path = asksaveasfilename(confirmoverwrite=True, defaultextension="png",
                             filetypes=[("png", ".png"), ("jpeg", ".jpg")])
    if path:
        textmark.result_image.save_btn(path)


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

text_size = Entry(width=5,)
text_size.pack()
text_size.insert(index=0, string=textmark.size)
text_size.bind("<KeyRelease>", update_text_size)
text_size.config(state="disabled")
# text_size.config(state="disabled")

# --------------------------------------------------------------------------------------------------------------------

# -------------------------------------image watermark --------------------------------------------------------------
image_radio_btn = ttk.Radiobutton(root, text="Image Water Mark", value="image", variable=radio_value, state="disabled",
                                  command=image_mark_active,)
image_radio_btn.pack()

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
