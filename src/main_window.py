from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QAction, QMenuBar, QLabel, QSlider
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
import numpy as np
from image_display_widget import ImageDisplayWidget
from image_list_widget import ImageListWidget
from PyQt5.QtWidgets import QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        
        self.image_display_widget = ImageDisplayWidget(main_window=self)
        self.image_list_widget = ImageListWidget()
        self.selected_images = []

        self.init_ui()

        self.offset = QPoint(0, 0)
        self.dragging = False
        self.last_pos = QPoint()

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

        # Add slider for rotation
        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setMinimum(-180)
        self.rotation_slider.setMaximum(180)
        self.rotation_slider.setValue(0)  # Initial value
        layout.addWidget(QLabel("Rotate:"))
        layout.addWidget(self.rotation_slider)

        # Add slider for zoom
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(0)
        self.zoom_slider.setMaximum(500)  # Adjust maximum zoom level as needed
        self.zoom_slider.setValue(100)  # Initial value (100%)
        layout.addWidget(QLabel("Zoom:"))
        layout.addWidget(self.zoom_slider)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.image_list_widget.imagesAdded.connect(self.update_image_display)
        self.weight_slider.valueChanged.connect(self.slider_changed)
        self.rotation_slider.valueChanged.connect(self.rotate_image)
        self.zoom_slider.valueChanged.connect(self.zoom_image)
        self.installEventFilter(self)

    def rotate_image(self):
        angle = self.rotation_slider.value()    
        selected_item = self.image_list_widget.currentItem().text()
        self.image_list_widget._data[selected_item].apply_rotation(angle)
        self.display_images()

    def zoom_image(self):
        zoom_level = self.zoom_slider.value() / 100.0
        # Implement zoom functionality here
        selected_item = self.image_list_widget.currentItem().text()
        self.image_list_widget._data[selected_item].zoom_image(zoom_level)
        self.display_images()
        
    def slider_changed(self):
        weight = self.weight_slider.value() / 100.0  # Normalize the slider value to a float between 0 and 1
        selected_item = self.image_list_widget.currentItem().text()
        self.image_list_widget._data[selected_item].change_transparency(weight)
        self.display_images()


    def update_image_display(self):
        self.selected_images.clear()
        for item in range(self.image_list_widget.count()):
            self.selected_images.append(self.image_list_widget.item(item).text())
        

        self.display_images()

    def display_images(self):
        combined_image = None    
        item = self.image_list_widget.currentItem()
        selected_item = None
        if item:
            selected_item = self.image_list_widget.currentItem().text() 
            combined_image =    self.image_list_widget._data[selected_item].modified_data
        for fp, reader in self.image_list_widget._data.items():
            if fp == selected_item:
                continue 
            image = reader.modified_data
            if combined_image is None:
                combined_image = image
            else:
                image = cv2.resize(image, (combined_image.shape[1], combined_image.shape[0]))
                combined_image = cv2.addWeighted(combined_image,0.5, image,0.5, 0) 


        self.image_display_widget.set_image(combined_image)

    def apply_offset(self, image):
         for reader in self.image_list_widget._data:            
            for reader.file_path in self.selected_images:
                reader.apply_shift(self.offset.x(), self.offset.y())
        

    def create_menu(self):
            menubar = self.menuBar()
            file_menu = menubar.addMenu('&File')

            open_action = QAction(QIcon.fromTheme("document-open"), '&Open', self)
            open_action.setStatusTip('Open JPEG Files')
            open_action.triggered.connect(self.image_list_widget.add_images)

            file_menu.addAction(open_action)


    def add_rotation_and_zoom_buttons(self):
        rotate_left_button = QPushButton('Rotate Left', self)
        rotate_left_button.clicked.connect(self.rotate_left)
        
        rotate_right_button = QPushButton('Rotate Right', self)
        rotate_right_button.clicked.connect(self.rotate_right)

        zoom_in_button = QPushButton('Zoom In', self)
        zoom_in_button.clicked.connect(self.zoom_in)

        zoom_out_button = QPushButton('Zoom Out', self)
        zoom_out_button.clicked.connect(self.zoom_out)

        layout = self.centralWidget().layout()
        layout.addWidget(rotate_left_button)
        layout.addWidget(rotate_right_button)
        layout.addWidget(zoom_in_button)
        layout.addWidget(zoom_out_button)

    def rotate_left(self):
        # Implement rotation left functionality
        pass

    def rotate_right(self):
        # Implement rotation right functionality
        pass

    def zoom_in(self):
        selected_item = self.image_list_widget.currentItem().text()
        self.image_list_widget._data[selected_item].zoom_in()
        self.display_images()

    def zoom_out(self):
        selected_item = self.image_list_widget.currentItem().text()
        self.image_list_widget._data[selected_item].zoom_out()
        self.display_images()