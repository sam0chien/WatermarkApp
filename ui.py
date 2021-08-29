import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from PIL import Image, ImageGrab

from photo import photo
from watermark import Watermark


class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = tk.Tk()
        self.root.title('Photo Watermark App')
        self.canvas = tk.Canvas(width=self.width, height=self.height)
        self.image = None
        self.fixed_height = height
        self.preview = None
        self.preview_image = tk.PhotoImage(file="preview.png")
        self.instruction_text = tk.StringVar()
        self.text_photo = tk.StringVar()
        self.text_watermark = tk.StringVar()
        self.font_name = 'Ariel'

    def ui(self):
        # Canvas
        self.canvas.grid(column=0, row=0, columnspan=4, padx=10, pady=10)
        # Photo Preview
        self.preview = self.canvas.create_image(self.width / 2, self.height / 2, image=self.preview_image)
        # Instruction Label
        instruction_label = tk.Label(textvariable=self.instruction_text, font=self.font_name)
        self.instruction_text.set('🌞 Please select a photo to watermark. 🌞')
        instruction_label.grid(columnspan=4, column=0, row=1)
        # Photo Button
        photo_btn = tk.Button(command=self.photo, textvariable=self.text_photo, font=self.font_name,
                              bg='gray', fg='black', height=2, width=15)
        self.text_photo.set('Photo')
        photo_btn.grid(column=0, row=2, pady=10)
        # Watermark Button
        wm_btn = tk.Button(command=self.watermark, textvariable=self.text_watermark, font=self.font_name,
                           bg='gray', fg='black', height=2, width=15)
        self.text_watermark.set('Watermark')
        wm_btn.grid(column=1, row=2, pady=10)
        # Save Button
        save_btn = tk.Button(command=self.save, text='Save', font=self.font_name, bg='gray',
                             fg='black', height=2, width=15)
        save_btn.grid(column=2, row=2, pady=10)
        # Cancel Button
        quit_btn = tk.Button(command=self.close, text='Quit', font=self.font_name, bg='gray',
                             fg='black', height=2, width=15)
        quit_btn.grid(column=3, row=2, pady=10)

        self.root.mainloop()

    def photo(self):
        photo_name = askopenfilename(initialdir='./', title='Select ⚙️', filetypes=(
            ('PNG', '*.png'), ('JPEG', ('*.jpg', '*.jpeg')), ('BMP', '*.bmp'), ('GIF', '*.gif')))
        if photo_name:
            self.image, self.preview_image = photo(photo_name, self.height)
            self.canvas.itemconfig(self.preview, image=self.preview_image)
            self.text_photo.set('Loaded')
            self.instruction_text.set('👀 Take a look. 👀')

    def watermark(self):
        watermark_name = askopenfilename(initialdir='./', title='Select ⚒️', filetypes=(
            ('JPEG', ('*.jpg', '*.jpeg')), ('PNG', '*.png'), ('BMP', '*.bmp'), ('GIF', '*.gif')))
        if watermark_name:
            Watermark(self.canvas, watermark_name, self.width / 2, self.height / 2)
            self.text_watermark.set('Loaded')

    # Bad quality output
    # def save(self):
    #     try:
    #         scale = (float(self.image.size[1]) / self.height)
    #         postscript = self.canvas.postscript(colormode='color')
    #         watermarked_image = Image.open(io.BytesIO(postscript.encode('utf-8')))
    #         watermarked_image.load(scale=ceil(scale))
    #         finished_img_name = asksaveasfilename(initialdir='output/', title='Save 🧸', filetypes=(
    #             ('PNG', '*.png'), ('JPEG', ('*.jpg', '*.jpeg')), ('BMP', '*.bmp'), ('GIF', '*.gif')))
    #         watermarked_image.save(finished_img_name)
    #         messagebox.showinfo(title='Success', message=f'File saved to {finished_img_name}❕')
    #         self.text_photo.set('Photo')
    #         self.text_watermark.set('Watermark')
    #     except AttributeError:
    #         messagebox.showwarning(title='Oops', message='Please upload a photo before save❗️')
    #     except ValueError:
    #         pass

    def save(self):
        if self.image:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            watermarked_image = ImageGrab.grab().crop((x, y, x1, y1))
            finished_img_name = asksaveasfilename(initialdir='output/', title='Save 🧸', filetypes=(
                ('PNG', '*.png'), ('JPEG', ('*.jpg', '*.jpeg')), ('BMP', '*.bmp'), ('GIF', '*.gif')))
            if finished_img_name:
                watermarked_image.resize((self.image.size[0], self.image.size[1]),
                                         Image.LANCZOS).convert('RGB').save(finished_img_name)
        else:
            messagebox.showwarning(title='Oops', message='Please upload a photo before save❗️')

    def close(self):
        leave = tk.messagebox.askyesno(message='Do you really wanna leave❓')
        if leave:
            self.root.destroy()
