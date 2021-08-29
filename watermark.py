from PIL import Image, ImageTk


class Watermark:
    def __init__(self, canvas, image, xpos, ypos):
        self.canvas = canvas
        self.image = Image.open(image).convert('RGBA')
        self.xpos, self.ypos = xpos, ypos
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_obj = canvas.create_image(xpos, ypos, image=self.tk_image)
        canvas.tag_bind(self.image_obj, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release)
        self.move_flag = False

    def move(self, event):
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y
            self.canvas.move(self.image_obj, new_xpos - self.mouse_xpos, new_ypos - self.mouse_ypos)
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.image_obj)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def release(self, event):
        self.move_flag = False
