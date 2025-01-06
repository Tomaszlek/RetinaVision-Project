from tkinter import filedialog, messagebox
import os
from PIL import Image

class FileLoader:
    def __init__(self, app, color_processor, blurring_processor, thresholding_processor, noise_reduction_processor,
                 morphology_processor, minutiae_processor):
        self.image_dir = None
        self.app = app
        self.color_processor = color_processor
        self.blurring_processor = blurring_processor
        self.thresholding_processor = thresholding_processor
        self.noise_reduction_processor = noise_reduction_processor
        self.morphology_processor = morphology_processor
        self.minutiae_processor = minutiae_processor

    def open_image(self):
      file_path = filedialog.askopenfilename(title="Select Image File",
                                             filetypes=[("Image Files", "*.ppm *.png *.jpg *.jpeg")])
      if file_path:
          self.load_image(file_path)
    def open_image_directory(self):
        self.image_dir = filedialog.askdirectory(title="Select Image Directory")
        if self.image_dir:
            messagebox.showinfo("Info", f"Image directory set to:\n{self.image_dir}")
            self.load_first_image()

    def load_first_image(self):
       if self.image_dir:
           ppm_files = [f for f in os.listdir(self.image_dir) if f.lower().endswith(".ppm")]
           if ppm_files:
              first_image_path = os.path.join(self.image_dir, ppm_files[0])
              self.load_image(first_image_path)
           else:
               messagebox.showerror("Error","No .ppm files found in the directory.")

    def load_image(self, image_path):
      try:
        image = Image.open(image_path)
        self.app.set_current_image(image)
        self.app.update_image_display()

      except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{e}")


class FileSaver:
    def __init__(self):
        self.results_dir = None

    def set_results_directory(self):
        self.results_dir = filedialog.askdirectory(title="Select Results Directory")
        if self.results_dir:
            messagebox.showinfo("Info", f"Results directory set to:\n{self.results_dir}")

    def save_image(self, image):
        if self.results_dir and image:
            file_path = filedialog.asksaveasfilename(title="Save Image",defaultextension=".png",filetypes=[("PNG files","*.png"),("JPEG files","*.jpg *.jpeg"), ("PPM files", "*.ppm")])
            if file_path:
                try:
                  image.save(file_path)
                except Exception as e:
                   messagebox.showerror("Error", f"Failed to save image:\n{e}")
        else:
            messagebox.showwarning("Warning","Please set results directory first and load an image")

class FileManager:
    def __init__(self, app, color_processor, blurring_processor, thresholding_processor, noise_reduction_processor,
                 morphology_processor, minutiae_processor):
        self.file_loader = FileLoader(app, color_processor, blurring_processor, thresholding_processor,
                                      noise_reduction_processor, morphology_processor, minutiae_processor)
        self.file_saver = FileSaver()
        self.app = app

    def open_image(self):
         self.file_loader.open_image()

    def open_image_directory(self):
        self.file_loader.open_image_directory()

    def set_results_directory(self):
        self.file_saver.set_results_directory()

    def save_image(self):
      if self.app.current_image:
        self.file_saver.save_image(self.app.current_image)