from PIL import Image
import numpy as np
from skimage.filters import threshold_local

class ThresholdingProcessor:
    def __init__(self, app, color_processor):
      self.app = app
      self.color_processor = color_processor

    def adaptive_threshold(self, image, block_size=21, method='gaussian', offset=5, invert_colors=False):
         if image is None:
           return None

         if len(np.array(image).shape) == 3:
           grayscale_image = self.color_processor.to_grayscale(image)
         else:
           grayscale_image = image

         gray_np = np.array(grayscale_image)

         if block_size % 2 == 0:
             block_size += 1
             print(f"Warning: block_size must be odd. Adjusting to {block_size}.")

         local_thresh = threshold_local(gray_np, block_size, method=method, offset=offset)

         binary_np = (gray_np > local_thresh).astype(np.uint8) * 255

         if invert_colors:
            binary_np = 255 - binary_np

         binary_image = Image.fromarray(binary_np)

         return binary_image # Return the result
