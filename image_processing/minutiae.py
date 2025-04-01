import numpy as np
from skimage.morphology import skeletonize
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu
from PIL import Image


class MinutiaeProcessor:
    def __init__(self, app):
        self.app = app

    def detect_minutiae(self, image):
        if image is None:
            return None, None

        image_np = np.array(image)
        if image_np.ndim == 3:  # Sprawdzenie, czy obraz jest kolorowy
            grayscale_image = self.app.color_processor.to_grayscale(image)
        else:
            grayscale_image = image

        image_np = np.array(grayscale_image)
        thresh = threshold_otsu(image_np)
        binary_image = image_np > thresh
        skeleton = skeletonize(binary_image)
        labeled_skeleton = label(skeleton)
        regions = regionprops(labeled_skeleton)
        minutiae = []

        for region in regions:
            coords = region.coords
            if len(coords) > 0:
                num_neighbors = self._count_neighbors(skeleton, coords[0])
                if num_neighbors == 1 or num_neighbors > 2:
                    minutiae.append(tuple(coords[0]))  # Konwersja do krotki dla bezpieczeństwa

        return minutiae, skeleton

    def remove_false_minutiae(self, minutiae, skeleton, distance_threshold=10):
        if not minutiae:
            return []

        valid_minutiae = []
        skeleton_np = np.array(skeleton)
        used_minutiae_indices = set()

        for i, min_coord1 in enumerate(minutiae):
            if i in used_minutiae_indices:
                continue

            is_valid = True
            for j, min_coord2 in enumerate(minutiae):
                if i == j or j in used_minutiae_indices:
                    continue

                distance = np.linalg.norm(np.array(min_coord1) - np.array(min_coord2))
                if distance < distance_threshold:
                    num_neighbors1 = self._count_neighbors(skeleton_np, min_coord1)
                    num_neighbors2 = self._count_neighbors(skeleton_np, min_coord2)

                    if num_neighbors1 > 2 and num_neighbors2 > 2:
                        is_valid = False
                        used_minutiae_indices.add(j)
                        break
                    elif num_neighbors1 == 1 and num_neighbors2 == 1:
                        is_valid = False
                        used_minutiae_indices.add(j)
                        break
                    else:
                        is_valid = False
                        used_minutiae_indices.add(j)
                        break

            if is_valid:
                valid_minutiae.append(min_coord1)
                used_minutiae_indices.add(i)

        return valid_minutiae

    def _count_neighbors(self, skeleton, coord):
        x, y = coord
        rows, cols = skeleton.shape
        count = 0

        for i in range(max(0, x - 1), min(rows, x + 2)):
            for j in range(max(0, y - 1), min(cols, y + 2)):
                if (i, j) != (x, y) and skeleton[i, j]:
                    count += 1

        return count

    def draw_minutiae_on_image(self, image, minutiae, skeleton):
        if image is None or not minutiae:
            return image

        image_np = np.array(image).copy()

        if image_np.ndim == 3:
            image_np.fill(255)  # Białe tło dla obrazów RGB

            for x, y in np.transpose(np.where(skeleton == 1)):
                if 0 <= x < image_np.shape[0] and 0 <= y < image_np.shape[1]:
                    image_np[x, y] = [0, 0, 0]  # Czarny kolor dla szkieletu

            for x, y in minutiae:
                for i in range(max(0, x - 1), min(image_np.shape[0], x + 2)):
                    for j in range(max(0, y - 1), min(image_np.shape[1], y + 2)):
                        image_np[i, j] = [255, 0, 0]  # Czerwony kolor dla minucji
        else:
            image_np.fill(255)  # Białe tło dla obrazów w skali szarości

            for x, y in np.transpose(np.where(skeleton == 1)):
                if 0 <= x < image_np.shape[0] and 0 <= y < image_np.shape[1]:
                    image_np[x, y] = 128  # Szary dla szkieletu

            '''for x, y in minutiae:
                for i in range(max(0, x - 1), min(image_np.shape[0], x + 2)):
                    for j in range(max(0, y - 1), min(image_np.shape[1], y + 2)):
                        image_np[i, j] = 0  # Czarny dla minucji*/'''

        minutiae_image = Image.fromarray(image_np)
        self.app.set_current_image(minutiae_image)
        self.app.update_image_display()

        return minutiae_image
