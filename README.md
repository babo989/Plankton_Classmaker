# Plankton Image Class Maker

A Python application built with PyQt5 for classifying segmented images of plankton from the Planktoscope, focusing on time lapse experiments. This tool helps researchers or enthusiasts quickly organize and label images by timepoints.

## Overview

The **Plankton Image Class Maker** provides an intuitive GUI that lets you:
- Select a main directory containing images, where each subdirectory represents a different timepoint.
- View segmented images and classify them into different categories using a simple interface.
- Easily manage and reorganize your image datasets.

This tool is especially useful for projects where images are collected over time and an efficient workflow is needed to sort and analyze the data before making object classifiers.

## Features

- **Graphical User Interface**: Built with PyQt5.
- **Directory Navigation**: Automatically detects subdirectories (each representing a timepoint).
- **Image Classification**: Allows you to assign classes to segmented plankton images.
- **File Management**: Uses Python’s standard libraries to move or copy files.

## Installation

### Prerequisites

- Python 3.6+  
- PyQt5 (for the GUI)

### Installation Steps

1. **Clone the repository**:

    git clone https://github.com/yourusername/PlanktonImageClassMaker.git
    cd PlanktonImageClassMaker

2. **Install Dependencies**:

    pip install PyQt5

## Usage

1. **Prepare Your Images**:  
   Ensure your main directory has subdirectories corresponding to different timepoints from your Planktoscope (e.g., `timepoint1`, `timepoint2`, etc.).

2. **Run the Application**:

    python ClassMaker.py

3. **Select the Main Directory**:  
   The GUI will prompt you to choose the folder that contains your directory containing the timepoint subdirectories.

4. **Classify Your Images**:  
   Browse the images, and use the on-screen controls to classify each image.

5. **Save or Move Files**:  
   The application can handle file operations as you classify images, keeping your dataset organized.

## Code Structure

- **ClassMaker.py**:  
  - Initializes the PyQt5 application.  
  - Manages directory selection and loading images from subdirectories.  
  - Provides user interaction for classification.  
  - Handles file operations (moving/copying files).

- **Dependencies**:  
  - Standard libraries: os, sys, shutil  
  - PyQt5 modules:  
    - QtWidgets (GUI components)  
    - QtGui (image handling and styling)  
    - QtCore (core functionalities)

## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch (e.g., `feature/my-feature`).
3. Commit your changes with descriptive messages.
4. Push your branch and open a pull request.

## License

This project is open source and available under an open license. See the [LICENSE](LICENSE) file for more information.

## Acknowledgements

- Powered by [PyQt5](https://pypi.org/project/PyQt5/).
- Thanks to the Planktoscope community and all contributors who help improve this project.

---


