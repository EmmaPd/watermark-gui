from PIL import Image, ImageShow
import PIL.Image
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning, showinfo

main_photo_url = ""
watermark_url = ""


def upload_main():
    global main_photo_url
    photo_url = askopenfilename(filetypes=(("JPEG files", "*.jpeg"), ("PNG files", "*.png")))
    main_photo_url = photo_url
    return main_photo_url


def upload_watermark():
    global watermark_url
    photo_url = askopenfilename(filetypes=(("JPEG files", "*.jpeg"), ("PNG files", "*.png")))
    watermark_url = photo_url
    return watermark_url


def merge_preview():
    global main_photo_url, watermark_url
    try:
        main_photo = PIL.Image.open(main_photo_url).convert("RGBA")
        watermark = PIL.Image.open(watermark_url).convert("RGBA")
    except AttributeError:
        showwarning(title="Error", message="Make sure you uploaded both photos first.")
    else:
        # Resize Watermark
        watermark_resized = watermark.resize(size=(round(main_photo.size[0] * 0.2), round(main_photo.size[1] * 0.2)))
        wm_mask = watermark_resized.convert("RGBA")

        # Determine position for watermark - lower right corner - needs refining* use a factor
        position = ((main_photo.size[0] - watermark_resized.size[0] - 20), (main_photo.size[1] - watermark_resized.size[1] - 20))

        # Transpose the watermark over a copy of the main photo
        merged_photo = main_photo.copy()
        merged_photo.paste(wm_mask, position, mask=wm_mask)

        ImageShow.show(merged_photo)


def save_photo():
    global main_photo_url, watermark_url
    try:
        main_photo = PIL.Image.open(main_photo_url).convert("RGBA")
        watermark = PIL.Image.open(watermark_url).convert("RGBA")
    except AttributeError:
        showwarning(title="Error", message="Make sure you uploaded both photos first.")

    else:
        # Resize Watermark
        watermark_resized = watermark.resize(size=(round(main_photo.size[0] * 0.2), round(main_photo.size[1] * 0.2)))
        wm_mask = watermark_resized.convert("RGBA")

        # Determine position for watermark - lower right corner - needs refining* use a factor
        position = ((main_photo.size[0] - watermark_resized.size[0] - 20), (main_photo.size[1] - watermark_resized.size[1] - 20))

        # Transpose the watermark over a copy of the main photo
        merged_photo = main_photo.copy()
        merged_photo.paste(wm_mask, position, mask=wm_mask)

        merged_photo.save("my-image-with-watermark.png")
        showinfo("Succes", "Your photo was successfully saved.\n Find it in the source folder.")

# Window
window = Tk()
window.title("Add a Watermark")
window.minsize(width=300, height=200)
window.config(padx=20, pady=20)

# Labels
main_img_label = Label(text="Main Image", font=("Calibri", 12, "bold"))
main_img_label.grid(column=0, row=1)
main_img_label.config(padx=15, pady=15)

watermark_img_label = Label(text="Watermark Image", font=("Calibri", 12, "bold"))
watermark_img_label.grid(column=0, row=2)
watermark_img_label.config(padx=15, pady=15)

# Buttons
button_main = Button(text="Upload Main Image", command=upload_main, width=20)
button_main.grid(column=1, row=1)

button_watermark = Button(text="Upload Watermark Image", command=upload_watermark, width=20)
button_watermark.grid(column=1, row=2)

merge = Button(text="Overlay & Preview", command=merge_preview, width=20, bg="snow")
merge.grid(column=0, row=3)

save = Button(text="Save image", command=save_photo, width=20, bg="coral")
save.grid(column=1, row=3)

window.mainloop()