# image_list_widget.py
from PyQt5.QtWidgets import QListWidget, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
import os
import cv2
import numpy as np


class ImageReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.original_data = None
        self.modified_data = None
        self.zoom_factor = 100
        self.read_image()

    def read_image(self):
        try:
            # Read the image using cv2
            self.original_data = cv2.imread(self.file_path)
            if self.original_data is None:
                raise FileNotFoundError(f"Could not read image at {self.file_path}")
            self.modified_data = np.copy(self.original_data)  # Copy original data for modifications
            return self.original_data
        except Exception as e:
            print(f"Error reading image: {e}")


    def zoom_image(self, zoom_factor):
        if zoom_factor <= 0:
            return
        width, height = self.original_data.shape[1], self.original_data.shape[0]

        new_width = int(self.original_data.shape[1] * zoom_factor )
        new_height = int(self.original_data.shape[0] * zoom_factor )
        dim = (width, height)

                # Calculate cropping dimensions to bring it back to the original size
        crop_width = min(new_width, width)
        crop_height = min(new_height, height)
        crop_x = (new_width - crop_width) // 2
        crop_y = (new_height - crop_height) // 2

        # Resize the image to the new width and height
        zoomed_image = cv2.resize(self.original_data, (new_width, new_height))

        # Crop the image to its original size
        zoomed_and_cropped_image = zoomed_image[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]

        # Set the zoomed and cropped image to the image reader
        self.modified_data = zoomed_and_cropped_image
        self.modified_data = cv2.resize(self.modified_data, dim, interpolation=cv2.INTER_LINEAR)

    def apply_rotation(self, angle):
          # Get the original image
        self.angle = angle
        original_image = self.original_data
        height, width = original_image.shape[:2]

        # Calculate the rotation center
        center = (width // 2, height // 2)

        # Perform the rotation
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(original_image, rotation_matrix, (width, height))

        # Add padding to restore original width and height
        max_dim = max(width, height)
        pad_x = (max_dim - width) // 2
        pad_y = (max_dim - height) // 2
        padded_image = cv2.copyMakeBorder(rotated_image, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=(0, 0, 0))

        # Set the padded image to the image reader
        self.modified_data = padded_image

    def apply_shift(self, dx, dy):
        if self.original_data is None:
            print("Image data not available. Please read the image first.")
            return
        rows, cols, _ = self.modified_data.shape
        translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])
        self.modified_data = cv2.warpAffine(self.modified_data, translation_matrix, (cols, rows))

    def reset_to_original(self):
        if self.original_data is None:
            print("Image data not available. Please read the image first.")
            return
        self.modified_data = np.copy(self.original_data)

    def change_transparency(self, alpha):

        # Create a transparent background image
        background = np.zeros_like(self.original_data)

        # Blend the image and background with transparency
        self.modified_data = cv2.addWeighted(self.original_data, alpha, background, 1 - alpha, 0)
    

class ImageListWidget(QListWidget):
    imagesAdded = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        self._data = {}

    def init_ui(self):
        pass

    def add_images(self):
        # Open file dialog to select images
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.jpg *.jpeg *.png)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            
            selected_files = file_dialog.selectedFiles()
            for file_path in selected_files:
                # Add each selected file to the list with full path
                self.addItem(file_path)
                self._data [file_path] =  ImageReader(file_path=file_path)
            self.imagesAdded.emit()
