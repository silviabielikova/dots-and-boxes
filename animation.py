from PIL import Image, ImageTk


class Animation:
    def __init__(self, x, y, canvas, file):
        self.canvas = canvas

        # image="", will change to individual frames in self.animate()
        self.gif = Image.open(file)
        self.image = self.canvas.create_image(x, y, image="")

        self.hide()
        self.img_list = []

        # moving: animation is either stopped or in motion
        self.moving = True
        self.i = 0

        while True:
            try:
                # to keep the transparency
                img = self.gif.copy().convert('RGBA')
                tk_img = ImageTk.PhotoImage(img)
                self.img_list.append(tk_img)
                self.i += 1
                self.gif.seek(self.i)
            except EOFError:
                break

        self.i = 0
        self.animate()

    def animate(self):
        self.canvas.itemconfig(self.image, image=self.img_list[self.i])
        self.canvas.update()
        if self.i == (len(self.img_list) - 1):
            self.i = 0
        else:
            self.i += 1
        if self.moving:
            self.canvas.after(50, self.animate)

    def stop(self):
        self.moving = False

    def hide(self):
        self.canvas.itemconfig(self.image, state='hidden')

    def show(self):
        self.canvas.itemconfig(self.image, state='normal')
