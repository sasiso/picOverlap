# main_window.py
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QAction, QMenuBar, QLabel, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import cv2
from image_display_widget import ImageDisplayWidget
from image_list_widget import ImageListWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        
        self.image_display_widget = ImageDisplayWidget()
        self.image_list_widget = ImageListWidget()
        self.selected_images = []

        self.init_ui()

    def init_ui(self):
        self.create_menu()

        main_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.image_display_widget, 70)
        layout.addWidget(self.image_list_widget, 20)

        # Add slider
        self.weight_slider = QSlider(Qt.Horizontal)
        self.weight_slider.setMinimum(0)
        self.weight_slider.setMaximum(100)
        self.weight_slider.setValue(50)  # Initial value
        layout.addWidget(QLabel("Adjust Weight:"))
        layout.addWidget(self.weight_slider)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.image_list_widget.imagesAdded.connect(self.update_image_display)
        self.weight_slider.valueChanged.connect(self.update_image_display)

    def update_image_display(self):
        self.selected_images.clear()
        for item in range(self.image_list_widget.count()):
            self.selected_images.append(self.image_list_widget.item(item).text())

        self.display_images()

    def display_images(self):
        combined_image = None
        weight = self.weight_slider.value() / 100.0  # Normalize the slider value to a float between 0 and 1
        for image_path in self.selected_images:
            image = cv2.imread(image_path)
            if combined_image is None:
                combined_image = image
            else:
                image = cv2.resize(image, (combined_image.shape[1], combined_image.shape[0]))
                combined_image = cv2.addWeighted(combined_image, 1 - weight, image, weight, 0)

        if combined_image is not None:
            self.image_display_widget.set_image(combined_image)

    def create_menu(self):
            menubar = self.menuBar()
            file_menu = menubar.addMenu('&File')

            open_action = QAction(QIcon.fromTheme("document-open"), '&Open', self)
            open_action.setStatusTip('Open JPEG Files')
            open_action.triggered.connect(self.image_list_widget.add_images)

            file_menu.addAction(open_action)