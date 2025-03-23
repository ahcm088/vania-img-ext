# OCR Text Extraction Project using EasyOCR with Sliding Window

This Python project is designed to extract text, including numbers, from images using EasyOCR with a sliding window approach. The project consists of two main files: `ocr_module.py` and `main.py`. The `ocr_module.py` file contains the core functionality for text extraction, while `main.py` provides a command-line interface to interact with the OCR module.

## Features

- **Text Extraction**: Extract text and numbers from images using EasyOCR with a sliding window.
- **Interactive Window Size Adjustment**: Allows users to interactively adjust the size of the sliding window for better text extraction.
- **Image Preprocessing**: Optionally preprocess images using OpenCV to enhance OCR accuracy.
- **Command-Line Interface**: Easily extract text from images via the command line.

## Requirements

To run this project, you need the following dependencies:

- Python 3.x
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) (Python wrapper for EasyOCR)
- [OpenCV](https://opencv.org/) (Optional, for image preprocessing)
- [Matplotlib](https://matplotlib.org/) (For displaying images during window size adjustment)
- [Torch](https://pytorch.org/) (CPU-only version)

Make sure you have installed the CPU-only version of PyTorch, torchvision, and torchaudio:

```bash
pip install torch torchvision torchaudio
```

Now, you can install the main Python dependencies using pip:

```bash
pip install easyocr opencv-python matplotlib
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

You can also specify the initial window size using the `--window_size` argument:

```bash
python main.py path/to/your/image.png --window_size 150 150
```

### Example

Suppose you have an image named `example.png` in the same directory as the script. You can extract text from it as follows:

```bash
python main.py example.png --preprocess --window_size 150 150
```

The script will output the extracted text to the console.

### Output

The script will print the extracted text to the console. The extracted text from each window will be saved in the `outputs/subfigs` directory as individual image files.

## Code Overview

### `ocr_module.py`

This module contains the `extract_text_with_window` and `get_user_window_size` functions, which perform the following tasks:

1. **Interactive Window Size Adjustment**: Allows the user to interactively adjust the size of the sliding window.
2. **Image Preprocessing (Optional)**: If the `preprocess` flag is enabled, the image is converted to grayscale and binarized using OpenCV to improve OCR accuracy.
3. **Text Extraction**: The processed or original image is passed to EasyOCR to extract text using a sliding window approach.
4. **Error Handling**: The function includes basic error handling to catch and report any issues during text extraction.

### `main.py`

This script provides a command-line interface for the OCR module. It uses the `argparse` library to parse command-line arguments and calls the `extract_text_with_window` and `get_user_window_size` functions from `ocr_module.py`.

## Directory Structure

```
.
├── ocr_module.py          # Core OCR functionality
├── main.py                # Command-line interface
├── outputs/               # Directory for processed images and subfigures (created automatically)
│   └── subfigs/           # Directory for individual window images
└── README.md              # This file
```

## Notes

- Ensure that the `outputs` directory exists or create it manually before running the script.
- Preprocessing is recommended for images with poor quality or complex backgrounds.
- The interactive window size adjustment feature allows for better control over the text extraction process.

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.

---