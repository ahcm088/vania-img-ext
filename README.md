# OCR Text Extraction Project using EasyOCR with DBSCAN Clustering

This Python project is designed to extract text, including numbers, from images using EasyOCR with DBSCAN clustering to group text regions. The project consists of two main files: `ocr_module.py` and `main.py`. The `ocr_module.py` file contains the core functionality for text extraction and grouping, while `main.py` provides a command-line interface to interact with the OCR module.

## Features

- **Text Extraction**: Extract text and numbers from images using EasyOCR.
- **Text Grouping**: Group detected text regions using DBSCAN clustering to reconstruct text order.
- **Image Preprocessing (Optional)**: Preprocess images using adaptive thresholding to enhance OCR accuracy.
- **Command-Line Interface**: Easily extract text from images via the command line.
- **Preprocessing Control**: Users can enable or disable preprocessing using the `--no-preprocess` flag.

## Requirements

To run this project, you need the following dependencies:

- Python 3.x
- [Torch](https://pytorch.org/) (CPU-only version, required for EasyOCR)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) (Python wrapper for EasyOCR)
- [OpenCV](https://opencv.org/) (For image preprocessing and bounding box visualization)
- [scikit-learn](https://scikit-learn.org/) (For DBSCAN clustering)

Install the required dependencies using pip:

```bash
pip install torch torchvision torchaudio
pip install easyocr opencv-python scikit-learn
```

## Usage

### Running the Script

To extract text from an image, use the `main.py` script with the following command:

```bash
python main.py path/to/your/image.png
```

#### Optional Flags:

- **Disable Preprocessing (`--no-preprocess`)**:  
  If you want to skip the preprocessing step and use the original image for OCR:
  
  ```bash
  python main.py path/to/your/image.png --no-preprocess
  ```

- **Adjust DBSCAN Clustering (`--eps <value>`)**:  
  You can also adjust the `eps` parameter for DBSCAN clustering (default is `50`) to control how closely text regions are grouped:

  ```bash
  python main.py path/to/your/image.png --eps 75
  ```

### Example

Suppose you have an image named `img4.png` in the `img/` folder in the project's directory. You can extract text from it as follows:

```bash
python main.py ./img/img4.png
```

Or with a custom `eps` value:

```bash
python main.py ./img/img4.png --eps 200
```

Or skipping preprocessing:

```bash
python main.py ./img/img4.png  --eps 200 --no-preprocess
```

The script will output the extracted and grouped text to the console.

### Output

The script will print the extracted and grouped text to the console. The cropped text regions and the image with bounding boxes will be saved in the `outputs/cropped_texts/` directory.

## Code Overview

### `ocr_module.py`

This module contains the following functions:

1. **`ensure_directory(directory)`**: Ensures the specified directory exists, creating it if necessary.
2. **`preprocess_image(image_path)`**: Applies adaptive thresholding to the image for better text detection.
3. **`group_text_boxes(results, original_image, save_dir, eps, min_samples)`**: Groups bounding boxes using DBSCAN clustering and saves cropped text regions and the image with bounding boxes.
4. **`extract_text_with_grouping(image_path, preprocess, eps)`**: Extracts text from the image, optionally preprocesses it, groups it using DBSCAN clustering, and returns the formatted grouped text.

### `main.py`

This script provides a command-line interface for the OCR module. It uses the `argparse` library to parse command-line arguments and calls the `extract_text_with_grouping` function from `ocr_module.py`.

## Directory Structure

```
.
├── ocr_module.py          # Core OCR functionality
├── main.py                # Command-line interface
├── outputs/               # Directory for processed images and cropped text regions (created automatically)
│   └── cropped_texts/     # Directory for cropped text regions and detected text image
└── README.md              # This file
```

## Notes

- Ensure that the `outputs` directory exists or create it manually before running the script.
- The `eps` parameter in DBSCAN clustering controls the proximity threshold for grouping text regions. Adjust it based on the image and text layout.
- **Preprocessing is optional**: You can disable it using the `--no-preprocess` flag.
- **Torch** is required for EasyOCR to function. If you encounter issues, ensure you have installed the correct version of Torch for your system.

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.
