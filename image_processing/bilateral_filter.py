import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

class BilateralFilterProcessor:
    def __init__(self, app):
        self.app = app

    def bilateral_filter(self, image, diameter=5, sigma_color=20, sigma_space=10):
        if image is None:
            return None

        image_np = np.array(image).astype(float)
        if len(image_np.shape) == 3:
            filtered_image_np = np.zeros_like(image_np)
            for i in range(3):
                filtered_image_np[:, :, i] = self._apply_bilateral(image_np[:,:,i], diameter, sigma_color, sigma_space)
            filtered_image = Image.fromarray(filtered_image_np.astype(np.uint8))
        else:
            filtered_image_np = self._apply_bilateral(image_np, diameter, sigma_color, sigma_space)
            filtered_image = Image.fromarray(filtered_image_np.astype(np.uint8))


        self.app.set_current_image(filtered_image)
        self.app.update_image_display()
        return filtered_image

    def _apply_bilateral(self, image, diameter, sigma_color, sigma_space):
        height, width = image.shape
        radius = diameter // 2
        filtered_image = np.zeros_like(image)

        for y in range(height):
            for x in range(width):
                i_filtered = 0
                w_sum = 0

                for j in range(max(0, y - radius), min(height, y + radius + 1)):
                    for i in range(max(0, x - radius), min(width, x + radius + 1)):
                        dist = np.sqrt((x - i)**2 + (y - j)**2)
                        if dist > radius:
                          continue

                        g_space = np.exp(-(dist**2) / (2 * sigma_space**2))
                        g_color = np.exp(-((image[y, x] - image[j, i])**2) / (2 * sigma_color**2))
                        w = g_space * g_color
                        i_filtered += image[j, i] * w
                        w_sum += w


                if w_sum > 0:
                    filtered_image[y, x] = i_filtered / w_sum


        return filtered_image