# OCR Text Extraction Project

This Python project is designed to extract text, including numbers, from images using Tesseract OCR. The project consists of two main files: `ocr_module.py` and `main.py`. The `ocr_module.py` file contains the core functionality for text extraction, while `main.py` provides a command-line interface to interact with the OCR module.

## Features

- **Text Extraction**: Extract text and numbers from images using Tesseract OCR.
- **Image Preprocessing**: Optionally preprocess images using OpenCV to enhance OCR accuracy.
- **Command-Line Interface**: Easily extract text from images via the command line.

## Requirements

To run this project, you need the following dependencies:

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) (Python Imaging Library)
- [pytesseract](https://pypi.org/project/pytesseract/) (Python wrapper for Tesseract OCR)
- [OpenCV](https://opencv.org/) (Optional, for image preprocessing)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (Must be installed on your system)

You can install the Python dependencies using pip:

```bash
pip install pillow pytesseract opencv-python
```

Additionally, make sure Tesseract OCR is installed on your system. You can download it from [here](https://github.com/tesseract-ocr/tesseract).

## Usage

### Running the Script

To extract text from an image, use the `main.py` script with the following command:

```bash
python main.py path/to/your/image.png
```

If you want to enable image preprocessing (recommended for noisy or low-quality images), use the `--preprocess` flag:

```bash
python main.py path/to/your/image.png --preprocess
```

### Example

Suppose you have an image named `example.png` in the same directory as the script. You can extract text from it as follows:

```bash
python main.py example.png --preprocess
```

The script will output the extracted text to the console.

### Output

The script will print the extracted text to the console. If preprocessing is enabled, the processed image will be saved in the `outputs` directory as `preprocess_img.png`.

## Code Overview

### `ocr_module.py`

This module contains the `extract_text` function, which performs the following tasks:

1. **Image Preprocessing (Optional)**: If the `preprocess` flag is enabled, the image is converted to grayscale and binarized using OpenCV to improve OCR accuracy.
2. **Text Extraction**: The processed or original image is passed to Tesseract OCR to extract text.
3. **Error Handling**: The function includes basic error handling to catch and report any issues during text extraction.

### `main.py`

This script provides a command-line interface for the OCR module. It uses the `argparse` library to parse command-line arguments and calls the `extract_text` function from `ocr_module.py`.

## Directory Structure

```
.
├── ocr_module.py          # Core OCR functionality
├── main.py                # Command-line interface
├── outputs/               # Directory for processed images (created automatically)
└── README.md              # This file
```

## Notes

- Ensure that the Tesseract executable is in your system's PATH or specify its location in the `pytesseract.pytesseract.tesseract_cmd` variable.
- Preprocessing is recommended for images with poor quality or complex backgrounds.

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.

---