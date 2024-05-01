# image_display_widget.py
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QImage, QColor
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtCore import Qt, QPoint, QRectF  # Import QRectF

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
            image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.strides[0], QImage.Format_RGB888)
            
            widget_rect = self.rect()
            image_rect = QRectF(image.rect())

            # Calculate aspect ratios
            aspect_ratio_widget = widget_rect.width() / widget_rect.height()
            aspect_ratio_image = image_rect.width() / image_rect.height()

            # Scale image to fit widget preserving aspect ratio
            if aspect_ratio_widget > aspect_ratio_image:
                # Fit image horizontally
                scaled_width = widget_rect.height() * aspect_ratio_image
                image_rect.setWidth(scaled_width)
                image_rect.setHeight(widget_rect.height())
            else:
                # Fit image vertically
                scaled_height = widget_rect.width() / aspect_ratio_image
                image_rect.setHeight(scaled_height)
                image_rect.setWidth(widget_rect.width())

            # Center image in widget
            image_rect.moveCenter(widget_rect.center())

            # Fill the area around the image with white color
            painter.fillRect(widget_rect, QColor('white'))

            # Draw image
            painter.drawImage(image_rect, image)


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
