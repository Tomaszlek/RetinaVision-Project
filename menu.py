import tkinter as tk
from tkinter import messagebox

class Menu:
    def __init__(self, root, file_manager):
        self.root = root
        self.file_manager = file_manager
        self.setup_menu()

    def setup_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Save Image", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Open Image Directory", command=self.open_image_directory)
        file_menu.add_command(label="Set Results Directory", command=self.set_results_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)


    def open_image(self):
         self.file_manager.open_image()


    def save_image(self):
        self.file_manager.save_image()

    def open_image_directory(self):
        self.file_manager.open_image_directory()

    def set_results_directory(self):
        self.file_manager.set_results_directory()

class SidePanel(tk.Frame):
    def __init__(self, parent, color_processor, blurring_processor, thresholding_processor, noise_reduction_processor, morphology_processor):
        super().__init__(parent, bg="#f0f0f0")
        self.color_processor = color_processor
        self.blurring_processor = blurring_processor
        self.thresholding_processor = thresholding_processor
        self.noise_reduction_processor = noise_reduction_processor
        self.morphology_processor = morphology_processor
        self.pack(side=tk.RIGHT, fill=tk.Y)

        self.setup_buttons()

    def setup_buttons(self):
         tk.Button(self, text="Convert to Grayscale", command=self.open_grayscale_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Blur Image", command=self.open_blur_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Subtract Blurred", command=self.open_subtract_blurred_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Otsu Thresholding", command=self.open_otsu_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Median Filter", command=self.open_median_filter_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Morphological Operations", command=self.open_morphology_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)




    def open_grayscale_options(self):
        GrayscaleOptions(self.master, self.color_processor)

    def open_blur_options(self):
        BlurOptions(self.master, self.blurring_processor)

    def open_subtract_blurred_options(self):
        SubtractBlurredOptions(self.master, self.blurring_processor, self.color_processor)
    def open_otsu_options(self):
      OtsuOptions(self.master, self.thresholding_processor)

    def open_median_filter_options(self):
      MedianFilterOptions(self.master, self.noise_reduction_processor)
    def open_morphology_options(self):
      MorphologyOptions(self.master, self.morphology_processor)


class GrayscaleOptions(tk.Toplevel):
    def __init__(self, parent, color_processor):
        super().__init__(parent)
        self.title("Grayscale Options")
        self.color_processor = color_processor

        self.channel_var = tk.StringVar(value="average")

        tk.Radiobutton(self, text="Red Channel", variable=self.channel_var, value="red").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Green Channel", variable=self.channel_var, value="green").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Blue Channel", variable=self.channel_var, value="blue").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Average", variable=self.channel_var, value="average").pack(anchor=tk.W)

        tk.Button(self, text="Convert", command=self.convert_to_grayscale).pack(pady=10)

    def convert_to_grayscale(self):
          channel = self.channel_var.get()
          self.color_processor.to_grayscale(channel=channel)
          self.destroy()

class BlurOptions(tk.Toplevel):
    def __init__(self, parent, blurring_processor):
         super().__init__(parent)
         self.title("Blur Options")
         self.blurring_processor = blurring_processor

         self.blur_type_var = tk.StringVar(value="box")
         self.window_size_var = tk.IntVar(value=3)

         tk.Label(self, text="Blur Type:").pack(anchor=tk.W)
         tk.Radiobutton(self, text="Box Blur", variable=self.blur_type_var, value="box").pack(anchor=tk.W)
         tk.Radiobutton(self, text="Gaussian Blur", variable=self.blur_type_var, value="gaussian").pack(anchor=tk.W)


         tk.Label(self, text="Window Size:").pack(anchor=tk.W)
         tk.Spinbox(self, from_=3, to=21, increment=2, textvariable=self.window_size_var).pack(anchor=tk.W)

         tk.Button(self, text="Blur", command=self.apply_blur).pack(pady=10)


    def apply_blur(self):
          blur_type = self.blur_type_var.get()
          window_size = self.window_size_var.get()
          if blur_type == "box":
              self.blurring_processor.box_blur(self.blurring_processor.app.current_image, window_size)
          elif blur_type == "gaussian":
             self.blurring_processor.gaussian_blur(self.blurring_processor.app.current_image, window_size)
          self.destroy()


class SubtractBlurredOptions(tk.Toplevel):
    def __init__(self, parent, blurring_processor, color_processor):
        super().__init__(parent)
        self.title("Subtract Blurred Options")
        self.blurring_processor = blurring_processor
        self.color_processor = color_processor

        self.blur_type_var = tk.StringVar(value="box")
        self.window_size_var = tk.IntVar(value=3)

        tk.Label(self, text="Blur Type:").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Box Blur", variable=self.blur_type_var, value="box").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Gaussian Blur", variable=self.blur_type_var, value="gaussian").pack(anchor=tk.W)


        tk.Label(self, text="Window Size:").pack(anchor=tk.W)
        tk.Spinbox(self, from_=3, to=21, increment=2, textvariable=self.window_size_var).pack(anchor=tk.W)

        tk.Button(self, text="Subtract", command=self.subtract_blurred).pack(pady=10)

    def subtract_blurred(self):
        blur_type = self.blur_type_var.get()
        window_size = self.window_size_var.get()
        image = self.color_processor.to_grayscale(self.blurring_processor.app.current_image)
        self.blurring_processor.app.set_current_image(image)
        self.blurring_processor.app.update_image_display()
        self.blurring_processor.subtract_blurred(window_size, blur_type)
        self.destroy()

class OtsuOptions(tk.Toplevel):
    def __init__(self, parent, thresholding_processor):
         super().__init__(parent)
         self.title("Otsu Thresholding Options")
         self.thresholding_processor = thresholding_processor
         self.invert_var = tk.BooleanVar(value=False)

         tk.Checkbutton(self, text="Invert Colors", variable=self.invert_var).pack(anchor=tk.W)
         tk.Button(self, text="Apply Otsu", command=self.apply_otsu).pack(pady=10)
    def apply_otsu(self):
       invert_colors = self.invert_var.get()
       otsu_image = self.thresholding_processor.otsu_threshold(self.thresholding_processor.app.current_image, invert_colors)
       if otsu_image is not None:
         self.thresholding_processor.app.set_current_image(otsu_image)
         self.thresholding_processor.app.update_image_display()
       self.destroy()

class MedianFilterOptions(tk.Toplevel):
    def __init__(self, parent, noise_reduction_processor):
        super().__init__(parent)
        self.title("Median Filter Options")
        self.noise_reduction_processor = noise_reduction_processor

        self.window_size_var = tk.IntVar(value=3)

        tk.Label(self, text="Window Size:").pack(anchor=tk.W)
        tk.Spinbox(self, from_=3, to=21, increment=2, textvariable=self.window_size_var).pack(anchor=tk.W)

        tk.Button(self, text="Apply Median Filter", command=self.apply_median_filter).pack(pady=10)
    def apply_median_filter(self):
        window_size = self.window_size_var.get()
        filtered_image = self.noise_reduction_processor.median_filter(self.noise_reduction_processor.app.current_image, size=window_size)
        if filtered_image is not None:
             self.noise_reduction_processor.app.set_current_image(filtered_image)
             self.noise_reduction_processor.app.update_image_display()
        self.destroy()

class MorphologyOptions(tk.Toplevel):
    def __init__(self, parent, morphology_processor):
        super().__init__(parent)
        self.title("Morphological Operations Options")
        self.morphology_processor = morphology_processor

        self.operation_var = tk.StringVar(value="closing")
        self.window_size_var = tk.IntVar(value=3)

        tk.Label(self, text="Operation:").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Closing", variable=self.operation_var, value="closing").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Opening", variable=self.operation_var, value="opening").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Max Filter", variable=self.operation_var, value="max").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Min Filter", variable=self.operation_var, value="min").pack(anchor=tk.W)

        tk.Label(self, text="Window Size:").pack(anchor=tk.W)
        tk.Spinbox(self, from_=3, to=21, increment=2, textvariable=self.window_size_var).pack(anchor=tk.W)
        tk.Button(self, text="Apply Operation", command=self.apply_operation).pack(pady=10)
    def apply_operation(self):
        operation_type = self.operation_var.get()
        window_size = self.window_size_var.get()
        if operation_type == "closing":
             self.morphology_processor.closing(self.morphology_processor.app.current_image, size = window_size)
        elif operation_type == "opening":
            self.morphology_processor.opening(self.morphology_processor.app.current_image, size = window_size)
        elif operation_type == "max":
            self.morphology_processor.max_filter(self.morphology_processor.app.current_image, size = window_size)
        elif operation_type == "min":
            self.morphology_processor.min_filter(self.morphology_processor.app.current_image, size = window_size)
        self.destroy()