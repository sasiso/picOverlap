# image_display_widget.py
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QImage, QColor
from PyQt5.QtCore import Qt, QPoint

class ImageDisplayWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()



    def init_ui(self):
        layout = QVBoxLayout()
        self.image_label = QLabel()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def set_image(self, image):
        self.image = image
        self.repaint()

    def paintEvent(self, event):
        if hasattr(self, 'image'):
            painter = QPainter(self)
            # Assuming self.image is a numpy.ndarray representing an image
            # Convert the numpy image to a QImage
            height, width, channel = self.image.shape
            bytesPerLine = channel * width
            qImg = QImage(self.image.data, width, height, bytesPerLine, QImage.Format_RGB888)

            # Fill the area around the image with white color
            painter.fillRect(self.rect(), QColor('white'))
            painter.drawImage(self.rect(),qImg)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.main_window.last_pos = event.pos()
            self.main_window.dragging = True

    def mouseMoveEvent(self, event):
        if self.main_window.dragging:
            delta = event.pos() - self.main_window.last_pos
            self.main_window.last_pos = event.pos()
            self.main_window.offset += delta
            self.main_window.display_images()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
