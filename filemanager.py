from tkinter import filedialog, messagebox
import os
from PIL import Image

class FileLoader:
    def __init__(self, app):
        self.image_dir = None
        self.app = app
        self.target_size = (550, 550)

    def open_image_directory(self):
        self.image_dir = filedialog.askdirectory(title="Select Image Directory")
        if self.image_dir:
            messagebox.showinfo("Info", f"Image directory set to:\n{self.image_dir}")

    def open_image(self):
        file_path = filedialog.askopenfilename(title="Select Image File",
                                               filetypes=[("Image Files", "*.ppm *.png *.jpg *.jpeg")])
        if file_path:
            self.load_image(file_path)

    def load_first_image(self):
        if self.image_dir:
            image_files = [f for f in os.listdir(self.image_dir) if
                           f.lower().endswith((".ppm", ".png", ".jpg", ".jpeg"))]
            if image_files:
                image_files.sort()
                first_image_path = os.path.join(self.image_dir, image_files[0])
                self.load_image(first_image_path)
            else:
                messagebox.showerror("Error", "No compatible image files found in the directory.")
        else:
            messagebox.showwarning("Warning", "Image directory not set.")


    def load_image(self, image_path):
        try:
            original_image = Image.open(image_path)

            print(f"Original image size: {original_image.size}")
            resized_image = original_image.resize(self.target_size, Image.Resampling.LANCZOS)
            print(f"Resized image size: {resized_image.size}")

            self.app.set_current_image(resized_image)
            self.app.update_image_display()

        except FileNotFoundError:
             messagebox.showerror("Error", f"Image file not found:\n{image_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load and resize image:\n{e}")


class FileSaver:
    def __init__(self):
        self.results_dir = None

    def set_results_directory(self):
        self.results_dir = filedialog.askdirectory(title="Select Results Directory")
        if self.results_dir:
            messagebox.showinfo("Info", f"Results directory set to:\n{self.results_dir}")

    def save_processed_image(self, image, filename):
        if self.results_dir and image:
            base, _ = os.path.splitext(filename)
            save_filename = f"{base}.png"
            save_path = os.path.join(self.results_dir, save_filename)
            try:
                image.save(save_path, format='PNG')
                print(f"Saved processed image to: {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image {save_filename}:\n{e}")
        elif not self.results_dir:
            messagebox.showwarning("Warning", "Results directory is not set. Cannot save image.")
        elif not image:
             messagebox.showwarning("Warning", "No image available to save.")


    def save_image(self, image):
        if image:
            file_path = filedialog.asksaveasfilename(title="Save Current Image", defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"),
                                                                ("PPM files", "*.ppm"), ("All files", "*.*")])
            if file_path:
                try:
                    image.save(file_path)
                    print(f"Saved current image to: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image:\n{e}")
        else:
            messagebox.showwarning("Warning", "No image is currently loaded to save.")


class FileManager:
    def __init__(self, app, side_panel):
        self.file_loader = FileLoader(app)
        self.file_saver = FileSaver()
        self.app = app
        self.side_panel = side_panel

    def process_all_images(self):
        if not self.file_loader.image_dir:
            messagebox.showwarning("Warning", "Please select an image directory first.")
            return

        if not self.file_saver.results_dir:
            messagebox.showwarning("Warning", "Please set a results directory first using 'File -> Set Results Directory'.")
            return


        image_files = [f for f in os.listdir(self.file_loader.image_dir) if
                       f.lower().endswith((".ppm", ".png", ".jpg", ".jpeg"))]

        if not image_files:
            messagebox.showwarning("Warning", "No compatible image files found in the selected directory.")
            return

        print(f"Found {len(image_files)} images to process in {self.file_loader.image_dir}")

        processed_count = 0
        error_count = 0
        for i, file_name in enumerate(image_files):
            image_path = os.path.join(self.file_loader.image_dir, file_name)
            print(f"\nProcessing image {i+1}/{len(image_files)}: {file_name}")

            try:
                self.file_loader.load_image(image_path)

                if self.app.current_image is None:
                    print(f"Skipping {file_name} due to loading error.")
                    error_count += 1
                    continue

                print(f"Running automatic sequence for {file_name}...")
                self.side_panel.run_automatic_sequence()
                print("Automatic sequence finished.")

                if self.app.current_image:
                    base, _ = os.path.splitext(file_name)
                    output_filename = f"processed_{base}.png"

                    print(f"Saving processed image as {output_filename}...")
                    self.file_saver.save_processed_image(self.app.current_image, output_filename)
                    processed_count += 1
                else:
                     print(f"Skipping save for {file_name} as processing might have failed (current_image is None).")
                     error_count +=1


            except Exception as e:
                error_count += 1
                messagebox.showerror("Processing Error", f"Failed to process {file_name}:\n{e}")
                print(f"Error processing {file_name}: {e}")

        messagebox.showinfo("Processing Complete", f"Finished processing all images.\nSuccessfully processed: {processed_count}\nErrors: {error_count}")
        print(f"\nProcessing complete. Success: {processed_count}, Errors: {error_count}")

    def open_image_directory(self):
        self.file_loader.open_image_directory()
        if self.file_loader.image_dir:
            self.file_loader.load_first_image()

    def set_results_directory(self):
        self.file_saver.set_results_directory()

    def open_image(self):
        self.file_loader.open_image()

    def save_image(self):
        if self.app.current_image:
            self.file_saver.save_image(self.app.current_image)
        else:
            messagebox.showwarning("Warning", "No image is currently loaded to save.")