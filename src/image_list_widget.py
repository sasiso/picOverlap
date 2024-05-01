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

    def apply_zoom(self, zoom_factor):
        if self.original_data is None:
            print("Image data not available. Please read the image first.")
            return
        self.modified_data = cv2.resize(self.modified_data, None, fx=zoom_factor, fy=zoom_factor)

    def apply_rotation(self, angle):
        if self.original_data is None:
            print("Image data not available. Please read the image first.")
            return
        rows, cols, _ = self.modified_data.shape
        rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        self.modified_data = cv2.warpAffine(self.modified_data, rotation_matrix, (cols, rows))

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
        self.weight = alpha
        if self.original_data is None:
            print("Image data not available. Please read the image first.")
            return
        self.modified_data = cv2.addWeighted(self.original_data, alpha, self.modified_data, 1 - alpha, 0)


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
