import tkinter.messagebox
from tkinter import *
from tkinter import ttk, colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.ttk import Style

from PIL import Image, ImageTk
from text_watermark import TextMark
from image_mark import ImageMark


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
    watermark_size.config(state="normal")

    rotation.set(textmark.rotation)
    watermark_size.delete(0, END)
    watermark_size.insert(1, textmark.size)

    textmark.image_to_make(image=BASE_IMAGE)
    textmark.make_final_image()

    display_result()


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
    rotation.set(image_mark.rotation)
    watermark_size.delete(0, END)
    watermark_size.insert(1, image_mark.current_size)
    image_mark.make_final_image()
    display_result()


def image_browse():
    # saving the file path of the image to be watermarked only jpeg or png can be selected
    filetype = (("JPG files", "*.jpg",), ("JPEG files", "*.jpeg",), ("PNG files", "*.png",))
    img_path = askopenfilename(initialdir="../Users/<name>/Pictures",
                               title="Select A File", filetypes=filetype)
    image_name = img_path.split("/")
    image_name = image_name[-1]
    image_label.config(text=image_name)
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
    else:
        image_mark.rotation = int(rotation.get())
        image_mark_active()


def update_opacity(new_value):
    opacity_label.config(text=f"{int(opacity.get())}%")

    if radio_value.get() == "text":
        textmark.opacity = int((255 * opacity.get() / 100))
        textmark_active()

    else:
        image_mark.opacity = int((255 * opacity.get() / 100))
        image_mark.update_opacity()
        image_mark_active()


def update_size():
    size = int(watermark_size.get())

    if radio_value.get() == "text":
        textmark.size = size
        textmark_active()
    else:
        image_mark.update_size(size=size)
        image_mark_active()


def display_result():
    global DISPLAY_IMAGE

    if radio_value.get() == "text":
        DISPLAY_IMAGE = textmark.result_image
    else:
        DISPLAY_IMAGE = image_mark.result_image

    DISPLAY_IMAGE.thumbnail(MAX_SIZE)
    DISPLAY_IMAGE = ImageTk.PhotoImage(DISPLAY_IMAGE)

    # canvas.config(width=720, height=560)
    canvas.create_image(460, 356, image=DISPLAY_IMAGE, anchor="center")
    canvas.image = DISPLAY_IMAGE


def add_more():
    global BASE_IMAGE
    if radio_value.get() == "text":
        BASE_IMAGE = textmark.result_image

    else:
        BASE_IMAGE = image_mark.result_image
        image_mark.put_default_mark()

    initial_process()


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
        watermark_size.config(state="readonly")
        move_up_btn.config(state="normal")
        move_down_btn.config(state="normal")
        move_left_btn.config(state="normal")
        move_right_btn.config(state="normal")
        reset_pos_btn.config(state="normal")
        save_btn.config(state="normal")
        add_mark.config(state="normal")
        BASE_IMAGE = Image.open(img_path)
        BASE_IMAGE = BASE_IMAGE.convert("RGBA")

        initial_process()


def initial_process():
    global BASE_IMAGE
    image_mark.receive_base_image(image=BASE_IMAGE)
    image_mark.make_default_pos()
    image_mark.update_opacity()

    radio_value.set("text")
    opacity.set(75)

    textmark.default_pos()
    textmark_active()


def move_up():
    if radio_value.get() == "text":
        textmark.move_up()
    else:
        image_mark.move_up()

    display_result()


def move_down():
    if radio_value.get() == "text":
        textmark.move_down()
    else:
        image_mark.move_down()
    display_result()


def move_left():
    if radio_value.get() == "text":
        textmark.move_left()
    else:
        image_mark.move_left()
    display_result()


def move_right():
    if radio_value.get() == "text":
        textmark.move_right()
    else:
        image_mark.move_right()
    display_result()


def default_position():
    rotation.set(0)
    if radio_value.get() == "text":
        textmark.default_pos()
        textmark_active()
    else:
        image_mark.make_default_pos()
        image_mark_active()


def save_image():
    # save image as a new file
    filetype = [("PNG files", ".png",), ("JPG files", ".jpg",), ("JPEG files", ".jpeg",)]
    path = asksaveasfilename(confirmoverwrite=True, defaultextension="png",
                             filetypes=filetype, title="Photo mark", initialfile="Photo mark image")
    if path:
        if radio_value.get() == "text":
            textmark.result_image.save(path)
        else:
            image_mark.result_image.save(path)
        tkinter.messagebox.showinfo(title="Success", message=f"File successfully saved at location\n{path}")




# ------------------------------------------- ui   --------------------------------------------------------------------

LITE_BLUE = "#D6DDF0"


root = Tk()
root.title("PhotoMark")
root.minsize(width=1280, height=760)
root.maxsize(width=1280, height=760)
icon = PhotoImage(file="./images/ui_images/icon.png")
root.iconphoto(False, icon)
style = Style()
style.theme_use("vista")
canvas = Canvas(root, width=1280, height=760)
canvas.place(x=0, y=0)
bg = PhotoImage(file="images/ui_images/reference.png")
background_image = canvas.create_image(640, 380, image=bg)

upload_btn_img = PhotoImage(file="./images/ui_images/upload.png")
upload_button = Button(root, image=upload_btn_img, command=upload_image, borderwidth=0, highlightthickness=0)
upload_button.place(x=96, y=665)

save_btn_img = PhotoImage(file="./images/ui_images/save.png")
save_btn = Button(root, image=save_btn_img, command=save_image, state="disabled", borderwidth=0, highlightthickness=0)
save_btn.place(x=1073, y=665)

add_more_btn_img = PhotoImage(file="./images/ui_images/add_more.png")
add_mark = Button(root, image=add_more_btn_img, command=add_more, state="disabled", borderwidth=0, highlightthickness=0)
add_mark.place(x=868, y=665)

radio_value = StringVar(value="text")

# ----------------------------------------------text watermark -----------------------------------------------------

text_radio_btn = ttk.Radiobutton(root, text="Text Water Mark", value="text", variable=radio_value, state="disabled",
                                 command=textmark_active, style="TRadiobutton" )
text_radio_btn.place(x=890, y=120)
style.configure("TRadiobutton", background=LITE_BLUE, fg="white",)

text_box = Entry(root, relief="flat", disabledbackground="white", disabledforeground=LITE_BLUE)
text_box.place(x=930, y=155)
text_box.bind("<KeyRelease>", update_textbox)
text_box.insert(index=1, string=textmark.text)
text_box.config(state="disabled")

current_font = StringVar()
fonts = ttk.Combobox(root, width=23, state="readonly", textvariable=current_font, background="white")
fonts["values"] = textmark.font_list
fonts.bind("<<ComboboxSelected>>", text_font_update)
fonts.place(x=928, y=221)
fonts.current(2)
fonts.config(state="disabled")

color_box = Button(root, width=5, borderwidth=0, background="white", state="disabled", command=update_text_color)
color_box.place(x=1108, y=221)

# --------------------------------------------------------------------------------------------------------------------

# -------------------------------------image watermark --------------------------------------------------------------
image_radio_btn = ttk.Radiobutton(root, text="Image Water Mark", value="image", variable=radio_value, state="disabled",
                                  command=image_mark_active, )
image_radio_btn.place(x=890, y=275)
image_label = Label(text="photo_mark.png", width=25, state="disabled", background="white",)
image_label.place(x=914, y=308)

browse_btn_image = PhotoImage(file="./images/ui_images/browse.png")
image_browse_btn = Button(root, image=browse_btn_image, command=image_browse, state="disabled", borderwidth=0,
                          highlightthickness=0, background=LITE_BLUE)
image_browse_btn.place(x=1051, y=298)

# -------------------------------------------------------------------------------------------------------------------

# ----------------------------------------common options----------------------------------------------------------


opacity = ttk.Scale(root, from_=0, to=100, length=65, command=update_opacity, state="disabled", value=75,
                    style="Horizontal.TScale")
opacity.place(x=895, y=483)
style.configure("Horizontal.TScale", background=LITE_BLUE)

opacity_label = Label(root, text=f"{opacity.get()}%", background="white",)
opacity_label.place(x=980, y=482)

watermark_size = ttk.Spinbox(from_=5, to=10, width=9, command=update_size, wrap=True, state="disabled",)
watermark_size.place(x=898, y=420)

rotation = ttk.Spinbox(root, width=9, from_=0, to=360, increment=30, command=update_rotation,
                       wrap=True, state="readonly", )
rotation.set(0)
rotation.config(state="disabled")
rotation.place(x=898, y=555)

# edit position button---------------------------------------------------------------------------------------------
up_btn_img = PhotoImage(file="./images/ui_images/up.png")
move_up_btn = Button(root, image=up_btn_img, command=move_up, state="disabled", borderwidth=0,
                     highlightthickness=0, background=LITE_BLUE)
move_up_btn.place(x=1120, y=438)

down_btn_img = PhotoImage(file="./images/ui_images/down.png")
move_down_btn = Button(root, image=down_btn_img, command=move_down, state="disabled", borderwidth=0,
                       highlightthickness=0, background=LITE_BLUE)

move_down_btn.place(x=1120, y=525)

left_btn_img = PhotoImage(file="./images/ui_images/left.png")
move_left_btn = Button(root, image=left_btn_img, command=move_left, state="disabled", borderwidth=0,
                       highlightthickness=0, background=LITE_BLUE)
move_left_btn.place(x=1069, y=481)

right_btn_img = PhotoImage(file="./images/ui_images/right.png")
move_right_btn = Button(root, image=right_btn_img, command=move_right, state="disabled", borderwidth=0,
                        highlightthickness=0, background=LITE_BLUE)
move_right_btn.place(x=1172, y=481)

reset_btn_img = PhotoImage(file="./images/ui_images/reset.png")
reset_pos_btn = Button(root, image=reset_btn_img, command=default_position, state="disabled", borderwidth=0,
                       highlightthickness=0, background=LITE_BLUE)
reset_pos_btn.place(x=1108, y=478)

# ----------------------------------------------------------------------------------------------------------------


root.mainloop()
