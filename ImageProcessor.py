from PIL import Image
import numpy as np
from scipy.signal import convolve2d

class ImageProcessor:
    def __init__(self, app):
        self.app = app
        self.current_image = None

    def set_current_image(self, image):
        self.current_image = image
        self.app.set_current_image(image)


    def update_image_display(self):
        self.app.update_image_display()

    def to_grayscale(self, image=None, channel='average'):
      if image is None:
        if self.current_image:
            image_np = np.array(self.current_image)
            if len(image_np.shape) == 3:
                if channel == 'red':
                    grayscale_np = image_np[:, :, 0]
                elif channel == 'green':
                    grayscale_np = image_np[:, :, 1]
                elif channel == 'blue':
                    grayscale_np = image_np[:, :, 2]
                else:  # average
                    grayscale_np = np.mean(image_np, axis=2).astype(np.uint8)


                grayscale_image = Image.fromarray(grayscale_np)
                return grayscale_image
            else:
              print("Image is already in grayscale")
              return self.current_image
        return None
      else:
        image_np = np.array(image)
        if len(image_np.shape) == 3:
            if channel == 'red':
                grayscale_np = image_np[:, :, 0]
            elif channel == 'green':
                grayscale_np = image_np[:, :, 1]
            elif channel == 'blue':
                grayscale_np = image_np[:, :, 2]
            else:  # average
                grayscale_np = np.mean(image_np, axis=2).astype(np.uint8)


            grayscale_image = Image.fromarray(grayscale_np)
            return grayscale_image
        else:
          print("Image is already in grayscale")
          return image

    def get_current_image(self):
      return self.current_image

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
            return blurred_image
        else:
            mask = np.ones((window_size, window_size)) / (window_size * window_size)
            blurred_image_np = convolve2d(image_np, mask, mode='same', boundary='fill', fillvalue=0)
            blurred_image = Image.fromarray(blurred_image_np.astype(np.uint8))
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
            return blurred_image
        else:
             x, y = np.mgrid[-window_size // 2 + 1:window_size // 2 + 1, -window_size // 2 + 1:window_size // 2 + 1]
             g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
             mask = g / g.sum()
             blurred_image_np = convolve2d(image_np, mask, mode='same', boundary='fill', fillvalue=0)
             blurred_image = Image.fromarray(blurred_image_np.astype(np.uint8))
             return blurred_image
    def subtract_blurred(self, window_size, blur_type):
         if self.current_image:
             original_image = self.current_image
             grayscale_image = self.to_grayscale(original_image)


             if blur_type == "box":
                 blurred_image = self.box_blur(grayscale_image,window_size)
             elif blur_type == "gaussian":
                blurred_image = self.gaussian_blur(grayscale_image, window_size)
             if blurred_image is None:
                return

             original_np = np.array(grayscale_image).astype(float)
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
             self.set_current_image(normalized_image)
             self.update_image_display()

    def otsu_threshold(self, image, invert_colors=False):
         if image is None:
           return None
         if len(np.array(image).shape) == 3:
           grayscale_image = self.to_grayscale(image)
         else:
           grayscale_image = image


         gray_np = np.array(grayscale_image).flatten()
         histogram, bins = np.histogram(gray_np, bins=256, range=(0, 256))

         total_pixels = len(gray_np)
         best_threshold = 0
         max_variance = 0

         for threshold in range(1, 255):
            w0 = np.sum(histogram[:threshold]) / total_pixels
            w1 = np.sum(histogram[threshold:]) / total_pixels
            if w0 == 0 or w1 == 0:
                 continue

            mu0 = np.sum(np.arange(threshold) * histogram[:threshold]) / np.sum(histogram[:threshold]) if np.sum(histogram[:threshold]) != 0 else 0
            mu1 = np.sum(np.arange(threshold, 256) * histogram[threshold:]) / np.sum(histogram[threshold:]) if np.sum(histogram[threshold:]) != 0 else 0

            variance = w0 * w1 * (mu0 - mu1)**2
            if variance > max_variance:
                max_variance = variance
                best_threshold = threshold


         binary_np = (np.array(grayscale_image) > best_threshold).astype(np.uint8) * 255

         if invert_colors:
            binary_np = 255 - binary_np
         binary_image = Image.fromarray(binary_np)
         return binary_image