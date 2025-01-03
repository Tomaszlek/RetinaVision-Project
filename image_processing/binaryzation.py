from PIL import Image
import numpy as np

class ThresholdingProcessor:
    def __init__(self, app, color_processor):
      self.app = app
      self.color_processor = color_processor

    def otsu_threshold(self, image, invert_colors=False):
         if image is None:
           return None
         if len(np.array(image).shape) == 3:
           grayscale_image = self.color_processor.to_grayscale(image)
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