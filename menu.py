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
    def __init__(self, parent, color_processor, blurring_processor, thresholding_processor, noise_reduction_processor,
                 morphology_processor, minutiae_processor, bilateral_processor):
        super().__init__(parent, bg="#f0f0f0")
        self.color_processor = color_processor
        self.blurring_processor = blurring_processor
        self.thresholding_processor = thresholding_processor
        self.noise_reduction_processor = noise_reduction_processor
        self.morphology_processor = morphology_processor
        self.minutiae_processor = minutiae_processor
        self.bilateral_processor = bilateral_processor
        self.pack(side=tk.RIGHT, fill=tk.Y)

        self.setup_buttons()

    def setup_buttons(self):
         # --- NEW START BUTTON ---
         tk.Button(self, text="Start Automatic Sequence", command=self.run_automatic_sequence, bg="#c0e0c0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5, ipady=5) # Added larger internal padding for emphasis
         # --- END NEW START BUTTON ---

         tk.Button(self, text="Convert to Grayscale", command=self.open_grayscale_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Blur Image", command=self.open_blur_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Subtract Blurred", command=self.open_subtract_blurred_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Otsu Thresholding", command=self.open_otsu_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Median Filter", command=self.open_median_filter_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Bilateral Filter", command=self.open_bilateral_options, bg="#e0e0e0", relief=tk.RAISED,
                   borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Morphological Operations", command=self.open_morphology_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)
         tk.Button(self, text="Detect Minutiae", command=self.open_minutiae_options, bg="#e0e0e0", relief=tk.RAISED, borderwidth=1, padx=5, pady=3).pack(fill=tk.X, pady=5)

    # --- NEW METHOD TO RUN THE SEQUENCE ---
    def run_automatic_sequence(self):
        """
        Runs the predefined sequence of image processing steps automatically.
        """
        current_app = self.color_processor.app # Get a reference to the app instance

        if current_app.current_image is None:
            messagebox.showwarning("No Image", "Please load an image first.")
            return

        try:
            print("Starting automatic sequence...")

            # 1. Convert to Grayscale (Green Channel)
            print("Step 1: Converting to Grayscale (Green Channel)")
            grayscale_image = self.color_processor.to_grayscale(image=current_app.current_image, channel='green')
            if grayscale_image is None:
                messagebox.showerror("Error", "Failed to convert to grayscale.")
                return
            current_app.set_current_image(grayscale_image) # Explicitly set image
            # No need to update display here, will happen implicitly or later

            # 2. Box Blur (Window Size 5)
            print("Step 2: Applying Box Blur (Size 5)")
            # box_blur modifies the app's current image internally and updates display
            self.blurring_processor.box_blur(current_app.current_image, window_size=5)
            if current_app.current_image is None: # Check if blur failed (though unlikely with current impl)
                 messagebox.showerror("Error", "Failed during Box Blur.")
                 return

            # 3. Subtract Blurred (Box Blur, Window Size 5)
            print("Step 3: Subtracting Blurred (Box Blur, Size 5)")
            # subtract_blurred modifies the app's current image internally and updates display
            self.blurring_processor.subtract_blurred(window_size=5, blur_type="box")
            if current_app.current_image is None:
                 messagebox.showerror("Error", "Failed during Subtract Blurred.")
                 return

            # 4. Median Filter (Window Size 3)
            print("Step 4: Applying Median Filter (Size 3)")
            # median_filter modifies the app's current image internally and updates display
            self.noise_reduction_processor.median_filter(current_app.current_image, size=3)
            if current_app.current_image is None:
                 messagebox.showerror("Error", "Failed during Median Filter.")
                 return

            # 5. Morphological Closing (Window Size 3)
            print("Step 5: Applying Morphological Closing (Size 3)")
            # closing modifies the app's current image internally and updates display
            self.morphology_processor.closing(current_app.current_image, size=3)
            if current_app.current_image is None:
                 messagebox.showerror("Error", "Failed during Closing.")
                 return

            # 6. Otsu Thresholding (No Inversion)
            print("Step 6: Applying Otsu Thresholding")
            # otsu_threshold returns the binary image, does NOT update app state
            binary_image = self.thresholding_processor.otsu_threshold(current_app.current_image, invert_colors=False)
            if binary_image is None:
                messagebox.showerror("Error", "Failed during Otsu Thresholding.")
                return
            current_app.set_current_image(binary_image) # Explicitly set image

            # 7. Detect and Filter Minutiae (Distance Threshold 1)
            print("Step 7: Detecting and Filtering Minutiae (Threshold 1)")
            # detect_minutiae uses the current (binary) image, returns results
            minutiae, skeleton = self.minutiae_processor.detect_minutiae(current_app.current_image)
            if minutiae is None or skeleton is None:
                 messagebox.showerror("Error", "Failed during Minutiae Detection.")
                 return

            # remove_false_minutiae uses results, returns filtered list
            filtered_minutiae = self.minutiae_processor.remove_false_minutiae(minutiae, skeleton, distance_threshold=1)

            # draw_minutiae_on_image uses the current (binary) image, filtered list,
            # and skeleton, and updates the app state and display internally.
            self.minutiae_processor.draw_minutiae_on_image(current_app.current_image, filtered_minutiae, skeleton)

            # Final explicit update just in case
            current_app.update_image_display()
            print("Automatic sequence finished.")
            messagebox.showinfo("Success", "Automatic processing sequence completed successfully!")

        except Exception as e:
            messagebox.showerror("Processing Error", f"An error occurred during the automatic sequence:\n{e}")
            print(f"Error during automatic sequence: {e}")
            # Optionally, try to reset to the original image or a safe state
            # current_app.set_current_image(original_image_backup) # Need to implement backup logic if desired
            current_app.update_image_display()

    # --- END NEW METHOD ---

    def open_grayscale_options(self):
        GrayscaleOptions(self.master, self.color_processor)

    def open_blur_options(self):
        BlurOptions(self.master, self.blurring_processor)

    def open_subtract_blurred_options(self):
        # Note: Subtract blurred now works on the current image, which might be color.
        # The manual button might need adjustment if it should *always* grayscale first.
        # The automatic sequence handles this explicitly.
        SubtractBlurredOptions(self.master, self.blurring_processor, self.color_processor)
    def open_otsu_options(self):
      OtsuOptions(self.master, self.thresholding_processor)

    def open_median_filter_options(self):
      MedianFilterOptions(self.master, self.noise_reduction_processor)

    def open_bilateral_options(self):
        BilateralFilterOptions(self.master, self.bilateral_processor)

    def open_morphology_options(self):
      MorphologyOptions(self.master, self.morphology_processor)

    def open_minutiae_options(self):
        MinutiaeOptions(self.master, self.minutiae_processor)


class GrayscaleOptions(tk.Toplevel):
    def __init__(self, parent, color_processor):
        super().__init__(parent)
        self.title("Grayscale Options")
        self.color_processor = color_processor
        self.app = self.color_processor.app # Get reference to app

        self.channel_var = tk.StringVar(value="average")

        tk.Radiobutton(self, text="Red Channel", variable=self.channel_var, value="red").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Green Channel", variable=self.channel_var, value="green").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Blue Channel", variable=self.channel_var, value="blue").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Average", variable=self.channel_var, value="average").pack(anchor=tk.W)

        tk.Button(self, text="Convert", command=self.convert_to_grayscale).pack(pady=10)

    def convert_to_grayscale(self):
          channel = self.channel_var.get()
          # Call to_grayscale without image arg, it will use app.current_image
          # and update the app state internally.
          self.color_processor.to_grayscale(channel=channel)
          self.destroy()

class BlurOptions(tk.Toplevel):
    def __init__(self, parent, blurring_processor):
         super().__init__(parent)
         self.title("Blur Options")
         self.blurring_processor = blurring_processor
         self.app = self.blurring_processor.app # Get reference to app


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
          if self.app.current_image is None:
              messagebox.showwarning("No Image", "Please load an image first.")
              self.destroy()
              return
          if blur_type == "box":
              # Methods update app state internally
              self.blurring_processor.box_blur(self.app.current_image, window_size)
          elif blur_type == "gaussian":
             # Methods update app state internally
             self.blurring_processor.gaussian_blur(self.app.current_image, window_size)
          self.destroy()


class SubtractBlurredOptions(tk.Toplevel):
    def __init__(self, parent, blurring_processor, color_processor):
        super().__init__(parent)
        self.title("Subtract Blurred Options")
        self.blurring_processor = blurring_processor
        self.color_processor = color_processor
        self.app = self.blurring_processor.app # Get reference to app


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

        if self.app.current_image is None:
              messagebox.showwarning("No Image", "Please load an image first.")
              self.destroy()
              return

        # --- Modification: Ensure grayscale before subtracting ---
        # The automatic sequence does this explicitly earlier. For the manual button,
        # we should probably ensure the image is grayscale *here* if it isn't already.
        current_img_np = self.app.current_image # Use numpy directly later if needed
        if len(np.array(current_img_np).shape) == 3:
            messagebox.showinfo("Info", "Converting to grayscale before subtracting blurred.")
            grayscale_image = self.color_processor.to_grayscale(image=self.app.current_image, channel='average') # Use average for manual case, or green? Let's stick to average.
            if grayscale_image:
                self.app.set_current_image(grayscale_image)
            else:
                 messagebox.showerror("Error", "Failed to convert image to grayscale for subtraction.")
                 self.destroy()
                 return
        # --- End Modification ---

        # This method updates the app state internally
        self.blurring_processor.subtract_blurred(window_size, blur_type)
        self.destroy()

class OtsuOptions(tk.Toplevel):
    def __init__(self, parent, thresholding_processor):
         super().__init__(parent)
         self.title("Otsu Thresholding Options")
         self.thresholding_processor = thresholding_processor
         self.app = self.thresholding_processor.app # Get reference to app
         self.invert_var = tk.BooleanVar(value=False)

         tk.Checkbutton(self, text="Invert Colors", variable=self.invert_var).pack(anchor=tk.W)
         tk.Button(self, text="Apply Otsu", command=self.apply_otsu).pack(pady=10)
    def apply_otsu(self):
       if self.app.current_image is None:
              messagebox.showwarning("No Image", "Please load an image first.")
              self.destroy()
              return
       invert_colors = self.invert_var.get()
       # otsu_threshold returns the image, need to set it manually
       otsu_image = self.thresholding_processor.otsu_threshold(self.app.current_image, invert_colors)
       if otsu_image is not None:
         self.app.set_current_image(otsu_image)
         self.app.update_image_display()
       else:
           messagebox.showerror("Error", "Otsu thresholding failed.")
       self.destroy()

class MedianFilterOptions(tk.Toplevel):
    def __init__(self, parent, noise_reduction_processor):
        super().__init__(parent)
        self.title("Median Filter Options")
        self.noise_reduction_processor = noise_reduction_processor
        self.app = self.noise_reduction_processor.app # Get reference to app

        self.window_size_var = tk.IntVar(value=3)
        self.window_size_var.trace("w", self.validate_window_size)

        tk.Label(self, text="Window Size:").pack(anchor=tk.W)
        tk.Spinbox(self, from_=3, to=21, increment=2, textvariable=self.window_size_var, validate="focusout", validatecommand=self.validate_window_size).pack(anchor=tk.W)
        tk.Button(self, text="Apply Median Filter", command=self.apply_median_filter).pack(pady=10)
    def validate_window_size(self, *args):
         try:
            value = self.window_size_var.get()
            if value % 2 == 0:
                # Ensure odd number
                self.window_size_var.set(max(3, value + 1 if value > 0 else 3)) # Ensure it's at least 3
         except tk.TclError:
             # Handle cases where the value might be temporarily invalid during input
            pass
         return True

    def apply_median_filter(self):
        if self.app.current_image is None:
              messagebox.showwarning("No Image", "Please load an image first.")
              self.destroy()
              return
        window_size = self.window_size_var.get()
        if window_size % 2 == 0 or window_size < 3:
            messagebox.showerror("Invalid Size", "Window size must be an odd number >= 3.")
            return # Keep window open

        # median_filter updates app state internally
        filtered_image = self.noise_reduction_processor.median_filter(self.app.current_image, size=window_size)
        # Check if it returned None (error) might be useful, though current implementation doesn't
        # if filtered_image is None:
        #    messagebox.showerror("Error", "Median filtering failed.")
        self.destroy()

class BilateralFilterOptions(tk.Toplevel):
    def __init__(self, parent, bilateral_processor):
        super().__init__(parent)
        self.title("Bilateral Filter Options")
        self.bilateral_processor = bilateral_processor
        self.app = self.bilateral_processor.app # Get reference to app

        self.diameter_var = tk.IntVar(value=5)
        self.sigma_color_var = tk.IntVar(value=20)
        self.sigma_space_var = tk.IntVar(value=10)

        tk.Label(self, text="Diameter:").pack(anchor=tk.W)
        tk.Spinbox(self, from_=3, to=15, textvariable=self.diameter_var, increment = 2).pack(anchor=tk.W)

        tk.Label(self, text="Sigma Color:").pack(anchor=tk.W)
        tk.Spinbox(self, from_=10, to=100, textvariable=self.sigma_color_var, increment = 5).pack(anchor=tk.W) # Increased max sigma color

        tk.Label(self, text="Sigma Space:").pack(anchor=tk.W)
        tk.Spinbox(self, from_=5, to=50, textvariable=self.sigma_space_var, increment = 5).pack(anchor=tk.W) # Increased max sigma space

        tk.Button(self, text="Apply Bilateral Filter", command=self.apply_bilateral_filter).pack(pady=10)

    def apply_bilateral_filter(self):
        if self.app.current_image is None:
              messagebox.showwarning("No Image", "Please load an image first.")
              self.destroy()
              return
        diameter = self.diameter_var.get()
        sigma_color = self.sigma_color_var.get()
        sigma_space = self.sigma_space_var.get()

        if diameter % 2 == 0 or diameter < 3:
            messagebox.showerror("Invalid Size", "Diameter must be an odd number >= 3.")
            return # Keep window open

        # bilateral_filter updates app state internally
        self.bilateral_processor.bilateral_filter(self.app.current_image, diameter, sigma_color, sigma_space)
        self.destroy()

class MorphologyOptions(tk.Toplevel):
    def __init__(self, parent, morphology_processor):
        super().__init__(parent)
        self.title("Morphological Operations Options")
        self.morphology_processor = morphology_processor
        self.app = self.morphology_processor.app # Get reference to app

        self.operation_var = tk.StringVar(value="closing")
        self.window_size_var = tk.IntVar(value=3)

        tk.Label(self, text="Operation:").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Closing", variable=self.operation_var, value="closing").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Opening", variable=self.operation_var, value="opening").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Max Filter (Dilation)", variable=self.operation_var, value="max").pack(anchor=tk.W) # Clarified name
        tk.Radiobutton(self, text="Min Filter (Erosion)", variable=self.operation_var, value="min").pack(anchor=tk.W) # Clarified name

        tk.Label(self, text="Window Size (Structure Element):").pack(anchor=tk.W) # Clarified label
        tk.Spinbox(self, from_=3, to=21, increment=2, textvariable=self.window_size_var).pack(anchor=tk.W)
        tk.Button(self, text="Apply Operation", command=self.apply_operation).pack(pady=10)
    def apply_operation(self):
        if self.app.current_image is None:
              messagebox.showwarning("No Image", "Please load an image first.")
              self.destroy()
              return
        operation_type = self.operation_var.get()
        window_size = self.window_size_var.get()

        if window_size % 2 == 0 or window_size < 3:
            messagebox.showerror("Invalid Size", "Window size must be an odd number >= 3.")
            return # Keep window open

        # All morphology methods update app state internally
        if operation_type == "closing":
             self.morphology_processor.closing(self.app.current_image, size = window_size)
        elif operation_type == "opening":
            self.morphology_processor.opening(self.app.current_image, size = window_size)
        elif operation_type == "max":
            self.morphology_processor.max_filter(self.app.current_image, size = window_size)
        elif operation_type == "min":
            self.morphology_processor.min_filter(self.app.current_image, size = window_size)
        self.destroy()

class MinutiaeOptions(tk.Toplevel):
    def __init__(self, parent, minutiae_processor):
        super().__init__(parent)
        self.title("Minutiae Options")
        self.minutiae_processor = minutiae_processor
        self.app = self.minutiae_processor.app # Get reference to app


        self.distance_threshold_var = tk.IntVar(value=10)
        tk.Label(self, text="False Minutiae Distance Threshold:").pack(anchor=tk.W) # Clarified label
        tk.Spinbox(self, from_=1, to=50, textvariable=self.distance_threshold_var).pack(anchor=tk.W) # Increased max

        tk.Button(self, text="Detect and Filter Minutiae", command=self.detect_and_filter_minutiae).pack(pady=10)

    def detect_and_filter_minutiae(self):
        if self.app.current_image is None:
              messagebox.showwarning("No Image", "Please load an image first.")
              self.destroy()
              return

        # --- Modification: Ensure binary image ---
        # Minutiae detection typically works best on a binary skeleton.
        # Check if the current image is binary, if not, warn or attempt Otsu.
        current_img_np = np.array(self.app.current_image)
        is_binary = len(current_img_np.shape) == 2 and np.all(np.isin(current_img_np, [0, 255])) # Simple check
        is_grayscale = len(current_img_np.shape) == 2 and not is_binary

        if len(current_img_np.shape) == 3: # Color image
            messagebox.showwarning("Image Type", "Minutiae detection requires a binary image. Please apply Otsu Thresholding first.")
            self.destroy()
            return
        elif is_grayscale: # Grayscale but not binary
             messagebox.showwarning("Image Type", "Minutiae detection works best on a binary image. Please apply Otsu Thresholding first (or ensure image is already binary).")
             # Optionally, could automatically apply Otsu here, but better to guide user.
             # otsu_img = self.minutiae_processor.app.thresholding_processor.otsu_threshold(self.app.current_image)
             # if otsu_img: self.app.set_current_image(otsu_img) else: return
             self.destroy()
             return
        # --- End Modification ---


        distance_threshold = self.distance_threshold_var.get()
        if distance_threshold < 0:
            messagebox.showerror("Invalid Value", "Distance threshold cannot be negative.")
            return # Keep window open

        # detect_minutiae uses current (binary), returns results
        minutiae, skeleton = self.minutiae_processor.detect_minutiae(self.app.current_image)

        if minutiae is None or skeleton is None:
            messagebox.showerror("Error", "Minutiae detection failed. Ensure image is binary/skeletonizable.")
            self.destroy()
            return

        # remove_false_minutiae uses results, returns filtered list
        filtered_minutiae = self.minutiae_processor.remove_false_minutiae(minutiae, skeleton, distance_threshold)

        # draw_minutiae_on_image uses current (binary), filtered list, skeleton, updates app state
        self.minutiae_processor.draw_minutiae_on_image(self.app.current_image, filtered_minutiae, skeleton)

        self.destroy()

# --- Need to import numpy in menu.py for the checks ---
import numpy as np
# --- End Import ---