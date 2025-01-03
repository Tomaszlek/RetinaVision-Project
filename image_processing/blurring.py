from PIL import Image
import numpy as np
from scipy.signal import convolve2d

class BlurringProcessor:
    def __init__(self, app):
        self.app = app

    def box_blur(self, image, window_size):
        if image is None:
             return None
        image_np = np.array(image).astype(float)
        if len(image_np.shape) == 3:
            mask = np.ones((window_size, window_size)) / (window_size * window_size)
            blurred_image_np = np.zeros_like(image_np)
            for i in range(3):
                blurred_image_np[:,:,i] = convolve2d(image_np[:,:,i],mask, mode='same', boundary='fill', fillvalue=0)
            blurred_image = Image.fromarray(blurred_image_np.astype(np.uint8))
            self.app.set_current_image(blurred_image)
            self.app.update_image_display()
            return blurred_image
        else:
            mask = np.ones((window_size, window_size)) / (window_size * window_size)
            blurred_image_np = convolve2d(image_np, mask, mode='same', boundary='fill', fillvalue=0)
            blurred_image = Image.fromarray(blurred_image_np.astype(np.uint8))
            self.app.set_current_image(blurred_image)
            self.app.update_image_display()
            return blurred_image
    def gaussian_blur(self, image, window_size, sigma=1.0):
        if image is None:
             return None
        image_np = np.array(image).astype(float)
        if len(image_np.shape) == 3:
            x, y = np.mgrid[-window_size // 2 + 1:window_size // 2 + 1, -window_size // 2 + 1:window_size // 2 + 1]
            g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
            mask = g / g.sum()
            blurred_image_np = np.zeros_like(image_np)
            for i in range(3):
               blurred_image_np[:,:,i] = convolve2d(image_np[:,:,i], mask, mode='same', boundary='fill', fillvalue=0)
            blurred_image = Image.fromarray(blurred_image_np.astype(np.uint8))
            self.app.set_current_image(blurred_image)
            self.app.update_image_display()
            return blurred_image
        else:
             x, y = np.mgrid[-window_size // 2 + 1:window_size // 2 + 1, -window_size // 2 + 1:window_size // 2 + 1]
             g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
             mask = g / g.sum()
             blurred_image_np = convolve2d(image_np, mask, mode='same', boundary='fill', fillvalue=0)
             blurred_image = Image.fromarray(blurred_image_np.astype(np.uint8))
             self.app.set_current_image(blurred_image)
             self.app.update_image_display()
             return blurred_image

    def subtract_blurred(self, window_size, blur_type):
        if self.app.current_image:
            original_image = self.app.current_image

            if blur_type == "box":
                blurred_image = self.box_blur(original_image, window_size)
            elif blur_type == "gaussian":
                blurred_image = self.gaussian_blur(original_image, window_size)
            if blurred_image is None:
                return

            original_np = np.array(original_image).astype(float)
            blurred_np = np.array(blurred_image).astype(float)

            print("Original image array:", original_np)
            print("Blurred image array:", blurred_np)

            subtracted_np = original_np - blurred_np
            print("Subtracted image array:", subtracted_np)

            min_val = np.min(subtracted_np)
            max_val = np.max(subtracted_np)
            print("Min value:", min_val)
            print("Max value:", max_val)
            if min_val != max_val:
                normalized_np = (subtracted_np - min_val) / (max_val - min_val) * 255
            else:
                normalized_np = np.zeros_like(subtracted_np)
            print("Normalized image array:", normalized_np)

            normalized_image = Image.fromarray(normalized_np.astype(np.uint8))
            self.app.set_current_image(normalized_image)
            self.app.update_image_display()