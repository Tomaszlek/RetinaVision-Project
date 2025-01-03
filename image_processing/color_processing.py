from PIL import Image
import numpy as np

class ColorProcessor:
    def __init__(self, app):
        self.app = app
        self.current_image = None

    def set_current_image(self, image):
      self.current_image = image
      self.app.set_current_image(image)

    def to_grayscale(self, image=None, channel='average'):
      if image is None:
        if self.app.current_image:
            image_np = np.array(self.app.current_image)
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
                self.set_current_image(grayscale_image)
                self.app.update_image_display()
                return grayscale_image
            else:
              print("Image is already in grayscale")
              return self.app.current_image
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