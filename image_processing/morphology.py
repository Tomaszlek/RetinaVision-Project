from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion, grey_dilation, grey_erosion

class MorphologyProcessor:
    def __init__(self, app):
        self.app = app
    def closing(self, image, size=3):
        if image is None:
             return None

        image_np = np.array(image).astype(np.uint8)
        if len(image_np.shape) == 3:
            mask = np.ones((size, size), dtype=np.uint8)
            closed_image_np = np.zeros_like(image_np)
            for i in range(3):
                dilated_image = grey_dilation(image_np[:,:,i], structure=mask).astype(np.uint8)
                closed_image_np[:,:,i]  = grey_erosion(dilated_image, structure=mask).astype(np.uint8)

            closed_image = Image.fromarray(closed_image_np)
            self.app.set_current_image(closed_image)
            self.app.update_image_display()
            return closed_image
        else:
            mask = np.ones((size,size), dtype = np.uint8)
            dilated_image = grey_dilation(image_np, structure = mask).astype(np.uint8)
            closed_image_np = grey_erosion(dilated_image, structure = mask).astype(np.uint8)
            closed_image = Image.fromarray(closed_image_np)
            self.app.set_current_image(closed_image)
            self.app.update_image_display()
            return closed_image


    def opening(self, image, size=3):
         if image is None:
             return None
         image_np = np.array(image).astype(np.uint8)
         if len(image_np.shape) == 3:
            mask = np.ones((size, size), dtype=np.uint8)
            opened_image_np = np.zeros_like(image_np)
            for i in range(3):
                eroded_image = grey_erosion(image_np[:,:,i], structure=mask).astype(np.uint8)
                opened_image_np[:,:,i] = grey_dilation(eroded_image, structure = mask).astype(np.uint8)
            opened_image = Image.fromarray(opened_image_np)
            self.app.set_current_image(opened_image)
            self.app.update_image_display()
            return opened_image
         else:
            mask = np.ones((size, size), dtype=np.uint8)
            eroded_image = grey_erosion(image_np, structure=mask).astype(np.uint8)
            opened_image_np = grey_dilation(eroded_image, structure = mask).astype(np.uint8)
            opened_image = Image.fromarray(opened_image_np)
            self.app.set_current_image(opened_image)
            self.app.update_image_display()
            return opened_image

    def max_filter(self, image, size=3):
      if image is None:
          return None
      image_np = np.array(image).astype(np.uint8)
      if len(image_np.shape) == 3:
        mask = np.ones((size, size), dtype=np.uint8)
        max_filtered_image_np = np.zeros_like(image_np)
        for i in range(3):
           max_filtered_image_np[:,:,i] = grey_dilation(image_np[:,:,i], structure = mask).astype(np.uint8)
        max_filtered_image = Image.fromarray(max_filtered_image_np)
        self.app.set_current_image(max_filtered_image)
        self.app.update_image_display()
        return max_filtered_image
      else:
          mask = np.ones((size, size), dtype = np.uint8)
          max_filtered_image_np = grey_dilation(image_np, structure = mask).astype(np.uint8)
          max_filtered_image = Image.fromarray(max_filtered_image_np)
          self.app.set_current_image(max_filtered_image)
          self.app.update_image_display()
          return max_filtered_image
    def min_filter(self, image, size=3):
         if image is None:
           return None
         image_np = np.array(image).astype(np.uint8)
         if len(image_np.shape) == 3:
           mask = np.ones((size, size), dtype=np.uint8)
           min_filtered_image_np = np.zeros_like(image_np)
           for i in range(3):
               min_filtered_image_np[:,:,i] = grey_erosion(image_np[:,:,i], structure = mask).astype(np.uint8)
           min_filtered_image = Image.fromarray(min_filtered_image_np)
           self.app.set_current_image(min_filtered_image)
           self.app.update_image_display()
           return min_filtered_image
         else:
           mask = np.ones((size, size), dtype=np.uint8)
           min_filtered_image_np = grey_erosion(image_np, structure = mask).astype(np.uint8)
           min_filtered_image = Image.fromarray(min_filtered_image_np)
           self.app.set_current_image(min_filtered_image)
           self.app.update_image_display()
           return min_filtered_image