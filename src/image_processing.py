import cv2
import numpy as np


class ImageReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.original_data = None
        self.modified_data = None
        self.zoom_factor = 0
        self.rotation = 0
        self.weight = 1
        self.dx = 0
        self.dy = 0
        self.changed = False
        self.read_image()

    def move_up(self):
        self.dy -= 10
        self.changed = True

    def move_down(self):
        self.dy += 10
        self.changed = True

    def move_left(self):
        self.dx -= 10
        self.changed = True

    def move_right(self):
        self.dx += 10
        self.changed = True

    def zoom_image(self, zoom_factor):
        self.changed = True
        self.zoom_factor = zoom_factor

    def apply_rotation(self, angle=None, re_apply_all=False):
        self.changed = True
        self.rotation = angle

    def read_image(self):
        try:
            # Read the image using cv2
            self.original_data = cv2.imread(self.file_path)
            if self.original_data is None:
                raise FileNotFoundError(f"Could not read image at {self.file_path}")

            self.modified_data = np.copy(
                self.original_data
            )  # Copy original data for modifications

            return self.original_data
        except Exception as e:
            print(f"Error reading image: {e}")

    def _zoom_image(self):
        zoom_factor = self.zoom_factor

        if zoom_factor <= 0:
            return

        width, height = self.modified_data.shape[1], self.modified_data.shape[0]

        new_width = int(self.modified_data.shape[1] * zoom_factor)
        new_height = int(self.modified_data.shape[0] * zoom_factor)

        if zoom_factor < 1:
            # If zooming out, create a blank image of original size
            zoomed_image = np.zeros(
                (height, width, self.modified_data.shape[2]), dtype=np.uint8
            )
            # Calculate the starting point for pasting the zoomed-out image
            start_x = (width - new_width) // 2
            start_y = (height - new_height) // 2
            # Paste the zoomed-out image onto the blank image
            zoomed_image[
                start_y : start_y + new_height, start_x : start_x + new_width
            ] = cv2.resize(self.modified_data, (new_width, new_height))
        else:
            # If zooming in, perform regular resizing and cropping
            dim = (width, height)
            # Calculate cropping dimensions to bring it back to the original size
            crop_width = min(new_width, width)
            crop_height = min(new_height, height)
            crop_x = (new_width - crop_width) // 2
            crop_y = (new_height - crop_height) // 2

            # Resize the image to the new width and height
            zoomed_image = cv2.resize(self.modified_data, (new_width, new_height))

            # Crop the image to its original size
            zoomed_image = zoomed_image[
                crop_y : crop_y + crop_height, crop_x : crop_x + crop_width
            ]

        # Resize the cropped image back to the original dimensions using linear interpolation
        self.modified_data = cv2.resize(
            zoomed_image, (width, height), interpolation=cv2.INTER_LINEAR
        )

    def _apply_rotation(
        self,
    ):
        # Get the original image
        angle = self.rotation
        height, width = self.modified_data.shape[:2]

        # Calculate the rotation center
        center = (width // 2, height // 2)

        # Perform the rotation
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(
            self.modified_data, rotation_matrix, (width, height)
        )

        # Add padding to restore original width and height
        max_dim = max(width, height)
        pad_x = (max_dim - width) // 2
        pad_y = (max_dim - height) // 2
        padded_image = cv2.copyMakeBorder(
            rotated_image,
            pad_y,
            pad_y,
            pad_x,
            pad_x,
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0),
        )

        # Set the padded image to the image reader
        self.modified_data = padded_image

    def _apply_shift(self):

        rows, cols, _ = self.original_data.shape
        translation_matrix = np.float32([[1, 0, self.dx], [0, 1, self.dy]])
        self.modified_data = cv2.warpAffine(
            self.original_data, translation_matrix, (cols, rows)
        )

        # Create a blank canvas with the same dimensions as the original image
        canvas = np.ones_like(self.original_data) * 255  # Fill with white pixels

        # Compute the offset to center the moved image on the canvas
        canvas_rows, canvas_cols, _ = canvas.shape
        offset_x = (canvas_cols - cols) // 2
        offset_y = (canvas_rows - rows) // 2

        # Paste the moved image onto the canvas
        canvas[offset_y : offset_y + rows, offset_x : offset_x + cols] = (
            self.modified_data
        )

        self.modified_data = canvas

    def reset_to_original(self):
        self.changed = False
        self.rotation = 0
        self.zoom_factor = 0
        self.dx = 0
        self.dy = 0
        if self.original_data is None:
            print("Image data not available. Please read the image first.")
            return
        self.modified_data = np.copy(self.original_data)

    def change_transparency(self, alpha):
        self.weight = alpha
        self.changed = True

    def _change_transparency(self):
        alpha = self.weight
        # Create a transparent background image
        background = np.zeros_like(self.modified_data)

        # Blend the image and background with transparency
        self.modified_data = cv2.addWeighted(
            self.modified_data, alpha, background, 1 - alpha, 0
        )

    def get_modified_data(self):

        if not self.changed:
            return self.modified_data

        self.modified_data = np.copy(
            self.original_data
        )  # Copy original data for modifications

        if self.changed:
            self.changed = False
            self._apply_shift()
            self._apply_rotation()
            self._zoom_image()
            self._change_transparency()

        return self.modified_data
