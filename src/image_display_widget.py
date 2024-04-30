# image_display_widget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout,QLabel
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class ImageDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_image(self, image):
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg.rgbSwapped())
        self.label.setPixmap(pixmap)
