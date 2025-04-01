import numpy as np
from PIL import Image

class AnisotropicDiffusionProcessor:
    def __init__(self, app):
        self.app = app

    def _diffusion_coeff(self, gradient, kappa, option=1):
        kappa = max(kappa, 1e-8)
        if option == 1:
            return np.exp(-(gradient / kappa)**2.)
        elif option == 2:
            return 1. / (1. + (gradient / kappa)**2.)
        else:
            raise ValueError("Option must be 1 or 2")

    def _apply_anisotropic_manual(self, image_np, n_iterations, kappa, gamma, option):
        diffused_image = image_np.astype(np.float64)
        rows, cols = diffused_image.shape

        for _ in range(n_iterations):
            padded_image = np.pad(diffused_image, 1, mode='edge')
            center = padded_image[1:-1, 1:-1]

            deltaN = padded_image[0:-2, 1:-1] - center
            deltaS = padded_image[2:  , 1:-1] - center
            deltaE = padded_image[1:-1, 2:  ] - center
            deltaW = padded_image[1:-1, 0:-2] - center

            cN = self._diffusion_coeff(np.abs(deltaN), kappa, option)
            cS = self._diffusion_coeff(np.abs(deltaS), kappa, option)
            cE = self._diffusion_coeff(np.abs(deltaE), kappa, option)
            cW = self._diffusion_coeff(np.abs(deltaW), kappa, option)

            divergence = (cN * deltaN +
                          cS * deltaS +
                          cE * deltaE +
                          cW * deltaW)

            diffused_image += gamma * divergence

        diffused_image = np.clip(diffused_image, 0, 255)
        return diffused_image.astype(np.uint8)


    def apply_anisotropic_diffusion(self, image, n_iterations=20, kappa=50, gamma=0.1, option=1):
        if image is None:
            return None

        if gamma > 0.25:
             print(f"Warning: Gamma ({gamma}) > 0.25 may lead to instability with this manual implementation. Reducing to 0.25.")
             gamma = 0.25

        image_np = np.array(image)

        filtered_image_np = np.zeros_like(image_np, dtype=np.uint8) # Final result is uint8

        if len(image_np.shape) == 3:
            for i in range(3):
                filtered_image_np[:, :, i] = self._apply_anisotropic_manual(
                    image_np[:, :, i],
                    n_iterations,
                    kappa,
                    gamma,
                    option
                )
        else:
             filtered_image_np = self._apply_anisotropic_manual(
                    image_np,
                    n_iterations,
                    kappa,
                    gamma,
                    option
                )

        filtered_image = Image.fromarray(filtered_image_np)

        self.app.set_current_image(filtered_image)
        self.app.update_image_display()
        return filtered_image