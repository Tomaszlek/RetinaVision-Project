import tkinter as tk
from menu import Menu, SidePanel
from filemanager import FileManager
from app import App
from image_processing.color_processing import ColorProcessor
from image_processing.blurring import BlurringProcessor
from image_processing.binaryzation import ThresholdingProcessor
from image_processing.noise_reduction import NoiseReductionProcessor
from image_processing.morphology import MorphologyProcessor
from image_processing.minutiae import MinutiaeProcessor
from image_processing.bilateral_filter import BilateralFilterProcessor

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RetinaVision")
        self.root.geometry("1366x768")

        self.app = App(self.root)
        self.color_processor = ColorProcessor(self.app)
        self.blurring_processor = BlurringProcessor(self.app)
        self.thresholding_processor = ThresholdingProcessor(self.app, self.color_processor)
        self.noise_reduction_processor = NoiseReductionProcessor(self.app)
        self.morphology_processor = MorphologyProcessor(self.app)
        self.minutiae_processor = MinutiaeProcessor(self.app)
        self.bilateral_processor = BilateralFilterProcessor(self.app)
        self.side_panel = SidePanel(self.root, self.color_processor, self.blurring_processor,
                                    self.thresholding_processor, self.noise_reduction_processor,
                                    self.morphology_processor,
                                    self.minutiae_processor, self.bilateral_processor)
        self.file_manager = FileManager(self.app, self.side_panel)
        self.menu = Menu(self.root, self.file_manager)



    def run(self):
      self.root.mainloop()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()