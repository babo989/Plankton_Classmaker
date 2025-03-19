#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 14:34:08 2025

@author: adam
"""


import os
import sys
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QFileDialog, QScrollArea, 
                             QGridLayout, QFrame, QMessageBox)
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt

class ImageBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.image_paths = []
        self.current_folder_index = 0
        self.folders = []
		# Change this to the categories that you will use as classes, folders will be created as subdirectories
        self.categories = ["New", "Dividing", "Pre_Division", "Vegetative", "Dead"]
        self.classification_dir = None
        self.classified_images = set()
        self.selected_images = set()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Planktoscope Object Viewer & Class Picker")
        self.setGeometry(100, 100, 1000, 800)

        self.folder_label = QLabel("No folder selected", self)
        self.folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.next_button = QPushButton("Next Folder", self)
        self.prev_button = QPushButton("Previous Folder", self)
        self.load_button = QPushButton("Load Directory", self)
        self.set_classification_dir_button = QPushButton("Set Classification Folder", self)

        self.next_button.clicked.connect(self.next_folder)
        self.prev_button.clicked.connect(self.prev_folder)
        self.load_button.clicked.connect(self.load_directory)
        self.set_classification_dir_button.clicked.connect(self.set_classification_directory)

        self.category_buttons = [QPushButton(cat, self) for cat in self.categories]
        for button in self.category_buttons:
            button.clicked.connect(self.move_selected_images_to_category)

        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.load_button)
        layout.addWidget(self.set_classification_dir_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)

        category_layout = QHBoxLayout()
        for button in self.category_buttons:
            category_layout.addWidget(button)
        layout.addLayout(category_layout)

        self.setLayout(layout)

    def load_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.folders = sorted([os.path.join(directory, d) for d in os.listdir(directory) 
                                   if os.path.isdir(os.path.join(directory, d))])
            if self.folders:
                self.current_folder_index = 0
                self.load_images_from_folder()

    def set_classification_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Classification Directory")
        if directory:
            self.classification_dir = directory
            for category in self.categories:
                os.makedirs(os.path.join(self.classification_dir, category), exist_ok=True)
            QMessageBox.information(self, "Success", f"Classification directory set to: {directory}\nSubfolders created for categories.")

    def load_images_from_folder(self):
        if not self.folders:
            return

        folder = self.folders[self.current_folder_index]
        self.folder_label.setText(f"Viewing: {os.path.basename(folder)}")
        self.image_paths = self.find_large_jpgs(folder)

        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for index, img_path in enumerate(self.image_paths):
            pixmap = QPixmap(img_path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
            label = QLabel(self)
            label.setPixmap(pixmap)
            label.setProperty("image_path", img_path)
            label.mousePressEvent = self.create_click_handler(label)

            if img_path in self.classified_images:
                palette = label.palette()
                palette.setColor(QPalette.ColorRole.Window, QColor('lightgreen'))
                label.setAutoFillBackground(True)
                label.setPalette(palette)

            self.grid_layout.addWidget(label, index // 5, index % 5)

    def create_click_handler(self, label):
        def handler(event):
            image_path = label.property("image_path")
            if image_path in self.selected_images:
                self.selected_images.remove(image_path)
                label.setStyleSheet("")  # Remove highlight of object
            else:
                self.selected_images.add(image_path)
                label.setStyleSheet("border: 3px solid red;")  # Highlight selected object
        return handler
	#This is just a threshold for images of interest, should adjust or improve 
    def find_large_jpgs(self, directory):
        return [os.path.join(directory, f) for f in sorted(os.listdir(directory))
                if f.endswith(".jpg") and os.path.getsize(os.path.join(directory, f)) > 10 * 1024]

    def move_selected_images_to_category(self):
        if not self.classification_dir:
            QMessageBox.warning(self, "Error", "Please set the classification directory first.")
            return

        sender = self.sender()
        category = sender.text()
        target_dir = os.path.join(self.classification_dir, category)
        os.makedirs(target_dir, exist_ok=True)

        for image_path in list(self.selected_images):
            if image_path and image_path not in self.classified_images:
                shutil.copy(image_path, target_dir)
                self.classified_images.add(image_path)
                self.selected_images.remove(image_path)

        self.load_images_from_folder()  # Refresh the display

        QMessageBox.information(self, "Success", f"Selected images copied to {target_dir}")

    def next_folder(self):
        if self.folders and self.current_folder_index < len(self.folders) - 1:
            self.current_folder_index += 1
            self.load_images_from_folder()

    def prev_folder(self):
        if self.folders and self.current_folder_index > 0:
            self.current_folder_index -= 1
            self.load_images_from_folder()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageBrowser()
    window.show()
    sys.exit(app.exec_())
