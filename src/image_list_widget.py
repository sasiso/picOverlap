# image_list_widget.py
from PyQt5.QtWidgets import QListWidget, QFileDialog
from PyQt5.QtCore import pyqtSignal

from image_processing import ImageReader


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
                self._data[file_path] = ImageReader(file_path=file_path)
            self.imagesAdded.emit()
