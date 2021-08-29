from PIL import Image, ImageTk


def photo(image, height):
    image = Image.open(image).convert('RGBA')
    height_percent = (height / float(image.size[1]))
    width_size = int((float(image.size[0]) * float(height_percent)))
    preview_image = ImageTk.PhotoImage(image.resize((width_size, height), Image.NEAREST))
    return image, preview_image
