from PIL import Image
import numpy as np
from scipy.signal import medfilt

class NoiseReductionProcessor:
     def __init__(self, app):
        self.app = app
     def median_filter(self, image, size=3):
        if image is None:
           return None
        image_np = np.array(image).astype(float)
        if len(image_np.shape) == 3:
            filtered_image_np = np.zeros_like(image_np)
            for i in range(3):
                filtered_image_np[:,:,i] = medfilt(image_np[:,:,i], kernel_size=size)
            filtered_image = Image.fromarray(filtered_image_np.astype(np.uint8))
            self.app.set_current_image(filtered_image)
            self.app.update_image_display()
            return filtered_image
        else:
            filtered_image_np = medfilt(image_np, kernel_size=size)
            filtered_image = Image.fromarray(filtered_image_np.astype(np.uint8))
            self.app.set_current_image(filtered_image)
            self.app.update_image_display()
            return filtered_image