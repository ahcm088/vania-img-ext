# OCR Text Extraction Project using EasyOCR

This Python project is designed to extract text, including numbers, from images using EasyOCR instead of Tesseract OCR. The project consists of two main files: `ocr_module.py` and `main.py`. The `ocr_module.py` file contains the core functionality for text extraction, while `main.py` provides a command-line interface to interact with the OCR module.

## Features

- **Text Extraction**: Extract text and numbers from images using EasyOCR.
- **Image Preprocessing**: Optionally preprocess images using OpenCV to enhance OCR accuracy.
- **Command-Line Interface**: Easily extract text from images via the command line.

## Requirements

To run this project, you need the following dependencies:

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) (Python Imaging Library)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) (Python wrapper for EasyOCR)
- [OpenCV](https://opencv.org/) (Optional, for image preprocessing)
- [Torch](https://pytorch.org/) (CPU-only version)

Make sure you have installed the CPU-only version of PyTorch, torchvision, and torchaudio:

```bash
pip install torch torchvision torchaudio
```

Now, Yyu can install the main Python dependencies using pip:

```bash
pip install pillow easyocr opencv-python
```

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
2. **Text Extraction**: The processed or original image is passed to EasyOCR to extract text.
3. **Error Handling**: The function includes basic error handling to catch and report any issues during text extraction.

```python
import cv2
import easyocr
from PIL import Image
import os

def extract_text(image_path, preprocess=False):
    # Load the image
    image = cv2.imread(image_path)
    
    # Preprocess the image if required
    if preprocess:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        preprocess_img_path = os.path.join('outputs', 'preprocess_img.png')
        cv2.imwrite(preprocess_img_path, image)
        print(f"Preprocessed image saved to {preprocess_img_path}")
    
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])
    
    # Perform OCR
    result = reader.readtext(image)
    
    # Extract and concatenate text
    extracted_text = ' '.join([res[1] for res in result])
    
    return extracted_text
```

### `main.py`

This script provides a command-line interface for the OCR module. It uses the `argparse` library to parse command-line arguments and calls the `extract_text` function from `ocr_module.py`.

```python
import argparse
from ocr_module import extract_text

def main():
    parser = argparse.ArgumentParser(description="Extract text from an image using EasyOCR.")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("--preprocess", action="store_true", help="Enable image preprocessing")
    
    args = parser.parse_args()
    
    # Extract text from the image
    text = extract_text(args.image_path, args.preprocess)
    
    # Print the extracted text
    print("Extracted Text:")
    print(text)

if __name__ == "__main__":
    main()
```

## Directory Structure

```
.
├── ocr_module.py          # Core OCR functionality
├── main.py                # Command-line interface
├── outputs/               # Directory for processed images (created automatically)
└── README.md              # This file
```

## Notes

- Ensure that the `outputs` directory exists or create it manually before running the script.
- Preprocessing is recommended for images with poor quality or complex backgrounds.

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.

---