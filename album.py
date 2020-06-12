"""
    A simple photo album viewer. The primary purpose of this app is to demonstrate the
    ability to use "smooth scrolling motion" on the canvas widget. A full photo app
    was not intended.

    Author: Israel Dryer
    Modified: 2020-06-11
"""

import os
import pathlib
import tkinter as tk

RIGHT = 'right'
LEFT = 'left'

class Album(tk.Tk):
    """Photo Album Viewer"""
    def __init__(self):
        super().__init__()
        self.title('Photo Album Viewer')
        self.geometry("500x500")
        self.iconbitmap("icon.ico")
        self.canvas = tk.Canvas(self, height=500, width=1500)
        self.img_index = 0
              
        # images
        imgpath = pathlib.Path() / 'Images'
        self.images = [tk.PhotoImage(file=imgpath / img) for img in os.listdir(imgpath)]
        self.empty = tk.PhotoImage(width=500, height=500)

        # # draw initial images on canvas
        self.draw_images()

        # adjust scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.xview_moveto(0.333)
        self.canvas.pack()

        # add binding
        self.bind("<Button-1>", self.on_click_next)
        self.bind("<Motion>", self.on_motion)

    def on_click_next(self, event):
        """Mouse button press callback"""
        if event.x < 50 and self.img_index > 0:
            self.draw_images()
            self.next_image(LEFT)
            self.img_index = self.img_index - 1
        elif event.x > 450 and self.img_index < len(self.images)-1:
            self.draw_images()
            self.next_image(RIGHT)
            self.img_index = self.img_index + 1
        else:
            return

    def on_motion(self, event):
        """Mouse motion callback"""
        if event.x < 50 and self.img_index > 0:
            self['cursor'] = 'left_side'
        elif event.x > 450 and self.img_index < len(self.images)-1:
            self['cursor'] = 'right_side'
        else:
            self['cursor'] = 'arrow'

    def draw_images(self):
        """Draw new images onto canvas"""
        self.canvas.delete('ALL')
        slots = (
            self.img_index - 1,
            self.img_index,
            self.img_index + 1)
        for slot, index in enumerate(slots):
            if index >= 0 and index < len(self.images):
                self.canvas.create_image(slot * 500, 0, image=self.images[index], anchor=tk.NW)
            else:
                self.canvas.create_image(slot * 500, 0, image=self.empty, anchor=tk.NW)
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))                
        self.canvas.xview_moveto(.333)            

    def viewport_right(self):
        """Move viewport to right"""
        x_left, _ = self.canvas.xview()
        if x_left < 0.666:
            new_position = min(x_left + 0.05, 0.666)
            self.canvas.xview_moveto(new_position)
            self.canvas.after(50, self.viewport_right)

    def viewport_left(self):
        """Move viewport to left"""
        x_left, _ = self.canvas.xview()
        if x_left > 0.0:
            new_position = max(x_left - 0.05, 0.0)
            self.canvas.xview_moveto(new_position)
            self.canvas.after(50, self.viewport_left)

    def next_image(self, direction):
        """Move viewport to next image"""
        if direction == RIGHT:
            self.viewport_right()
        elif direction == LEFT:
            self.viewport_left()
    

if __name__ == '__main__':

    a = Album()
    a.mainloop()