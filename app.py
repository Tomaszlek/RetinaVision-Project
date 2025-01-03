import tkinter as tk
from PIL import ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.current_image = None
        self.current_tk_image = None

        self.create_image_display()

    def create_image_display(self):
        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=10, pady=10, side=tk.LEFT, fill = tk.BOTH, expand=True)

    def set_current_image(self, image):
        self.current_image = image

    def update_image_display(self):
      if self.current_image:
        self.current_tk_image = ImageTk.PhotoImage(self.current_image)
        self.image_label.config(image=self.current_tk_image)
        self.image_label.image = self.current_tk_image
      else:
        self.image_label.config(image="")