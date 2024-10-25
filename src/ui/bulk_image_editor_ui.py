import sys
import threading

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog,
    QLineEdit, QComboBox, QCheckBox, QSpinBox, QColorDialog, QSlider, QHBoxLayout, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib import font_manager

from src.resizer import resize_images_maintain_aspect_ratio
from src.watermark import add_watermark


class BulkImageEditorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.font_paths = self.get_system_fonts()
        self.setWindowTitle("Bulk Image Editor")
        self.setGeometry(100, 100, 500, 600)
        self.init_ui()

    def init_ui(self):
        """
        Not really a beautiful UI, but it gets the job done.
        :return:
        """
        main_layout = QVBoxLayout()

        # Input Directory Section
        input_group = QGroupBox("Input/Output Directories")
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Input Directory"))
        self.input_directory = QLineEdit()
        input_layout.addWidget(self.input_directory)
        input_dir_button = QPushButton("Browse")
        input_dir_button.clicked.connect(self.browse_input_directory)
        input_layout.addWidget(input_dir_button)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Output Directory Section
        output_group = QGroupBox("Output Directory")
        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("Output Directory"))
        self.output_directory = QLineEdit()
        output_layout.addWidget(self.output_directory)
        output_dir_button = QPushButton("Browse")
        output_dir_button.clicked.connect(self.browse_output_directory)
        output_layout.addWidget(output_dir_button)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # Resize Options Section
        resize_group = QGroupBox("Resize Options")
        resize_layout = QVBoxLayout()
        self.resize_checkbox = QCheckBox("Resize Image")
        self.resize_checkbox.stateChanged.connect(self.toggle_resize_fields)
        resize_layout.addWidget(self.resize_checkbox)

        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Max Width"))
        self.max_width_spinbox = QSpinBox()
        self.max_width_spinbox.setRange(100, 5000)
        self.max_width_spinbox.setValue(800)
        self.max_width_spinbox.setEnabled(False)
        size_layout.addWidget(self.max_width_spinbox)
        size_layout.addWidget(QLabel("Max Height"))
        self.max_height_spinbox = QSpinBox()
        self.max_height_spinbox.setRange(100, 5000)
        self.max_height_spinbox.setValue(800)
        self.max_height_spinbox.setEnabled(False)
        size_layout.addWidget(self.max_height_spinbox)

        resize_layout.addLayout(size_layout)
        resize_group.setLayout(resize_layout)
        main_layout.addWidget(resize_group)

        # Watermark Options Section
        watermark_group = QGroupBox("Watermark Options")
        watermark_layout = QVBoxLayout()
        self.add_watermark_checkbox = QCheckBox("Add Watermark")
        self.add_watermark_checkbox.stateChanged.connect(self.toggle_watermark_fields)
        watermark_layout.addWidget(self.add_watermark_checkbox)

        watermark_layout.addWidget(QLabel("Watermark Text"))
        self.watermark_text = QLineEdit()
        self.watermark_text.setEnabled(False)
        watermark_layout.addWidget(self.watermark_text)

        watermark_layout.addWidget(QLabel("Font Size"))
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(6, 1000)
        self.font_size_spinbox.setValue(40)
        self.font_size_spinbox.setEnabled(False)
        watermark_layout.addWidget(self.font_size_spinbox)

        watermark_layout.addWidget(QLabel("Font Family"))
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(sorted(self.font_paths.keys()))
        self.font_family_combo.setEnabled(False)
        watermark_layout.addWidget(self.font_family_combo)

        watermark_layout.addWidget(QLabel("Watermark Image"))
        self.watermark_image = QLineEdit()
        self.watermark_image.setEnabled(False)
        watermark_layout.addWidget(self.watermark_image)
        self.watermark_image_dir_button = QPushButton("Browse")
        self.watermark_image_dir_button.clicked.connect(self.browse_watermark_image_directory)
        self.watermark_image_dir_button.setEnabled(False)
        watermark_layout.addWidget(self.watermark_image_dir_button)

        watermark_layout.addWidget(QLabel("Watermark Position"))
        self.position_combo = QComboBox()
        self.position_combo.addItems(["top-left", "top-right", "bottom-left", "bottom-right", "center"])
        self.position_combo.setEnabled(False)
        watermark_layout.addWidget(self.position_combo)

        watermark_layout.addWidget(QLabel("Watermark Transparency"))
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(0, 255)
        self.transparency_slider.setValue(128)
        self.transparency_slider.setEnabled(False)
        watermark_layout.addWidget(self.transparency_slider)

        self.fill_checkbox = QCheckBox("Fill entire image with watermark")
        self.fill_checkbox.setEnabled(False)
        watermark_layout.addWidget(self.fill_checkbox)

        color_picker_layout = QHBoxLayout()
        self.color_button = QPushButton("Select Watermark Color")
        self.color_button.clicked.connect(self.choose_watermark_color)
        self.color_button.setEnabled(False)
        color_picker_layout.addWidget(self.color_button)
        self.color_display = QLabel()
        self.color_display.setFixedSize(50, 50)
        self.color_display.setStyleSheet("border: 1px solid black;")
        self.color_display.setAutoFillBackground(True)
        color_picker_layout.addWidget(self.color_display)
        watermark_layout.addLayout(color_picker_layout)

        watermark_group.setLayout(watermark_layout)
        main_layout.addWidget(watermark_group)

        # Apply Button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_settings)
        main_layout.addWidget(apply_button)

        self.setLayout(main_layout)

    @staticmethod
    def get_system_fonts():
        fonts = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        font_families = {font_manager.FontProperties(fname=font).get_name(): font for font in fonts}
        return font_families

    def toggle_resize_fields(self, state):
        is_enabled = state == Qt.Checked
        self.max_width_spinbox.setEnabled(is_enabled)
        self.max_height_spinbox.setEnabled(is_enabled)
        self.add_watermark_checkbox.setChecked(not is_enabled)

    def toggle_watermark_fields(self, state):
        is_enabled = state == Qt.Checked
        self.watermark_text.setEnabled(is_enabled)
        self.font_size_spinbox.setEnabled(is_enabled)
        self.font_family_combo.setEnabled(is_enabled)
        self.watermark_image.setEnabled(is_enabled)
        self.position_combo.setEnabled(is_enabled)
        self.transparency_slider.setEnabled(is_enabled)
        self.fill_checkbox.setEnabled(is_enabled)
        self.color_button.setEnabled(is_enabled)
        self.watermark_image_dir_button.setEnabled(is_enabled)
        self.resize_checkbox.setChecked(not is_enabled)

    def browse_watermark_image_directory(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Watermark Image")
        if file:
            self.watermark_image.setText(file)

    def browse_input_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if directory:
            self.input_directory.setText(directory)

    def browse_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_directory.setText(directory)

    def choose_watermark_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_display.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            self.selected_color = color

    def apply_settings(self):
        input_dir = self.input_directory.text()
        output_dir = self.output_directory.text()
        if not input_dir or not output_dir:
            print("Please provide input and output directories.")
            return

        if self.resize_checkbox.isChecked():
            print("Resizing the images...")
            resize_images_thread = threading.Thread(
                target=resize_images_maintain_aspect_ratio,
                args=(
                    self.input_directory.text(),
                    self.output_directory.text(),
                    (self.max_width_spinbox.value(), self.max_height_spinbox.value())
                ))
            resize_images_thread.start()
        elif self.add_watermark_checkbox.isChecked():
            if not self.watermark_image.text() and not self.watermark_text.text():
                print("Please provide either watermark text or image.")
                return
            print("Adding watermark to the images...")
            text_color = self.selected_color.name() if hasattr(self, "selected_color") else "#FFFFFF"
            add_watermarks_thread = threading.Thread(
                target=add_watermark,
                args=(
                    self.input_directory.text(),
                    self.output_directory.text(),
                    self.watermark_text.text(),
                    self.watermark_image.text() if self.watermark_image.text() else None,
                    self.font_size_spinbox.value(),
                    self.font_paths.get(self.font_family_combo.currentText()),
                    text_color,
                    self.position_combo.currentText(),
                    self.transparency_slider.value() / 255.0,
                    self.fill_checkbox.isChecked()
                )
            )
            add_watermarks_thread.start()


if __name__ == "__main__":
    app = QApplication([])
    window = BulkImageEditorUI()
    window.show()
    sys.exit(app.exec())
