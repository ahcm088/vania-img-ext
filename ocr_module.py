import os
from PIL import Image
import pytesseract
import cv2

def extract_text(image_path, preprocess=False):
    """
    Extract text including numbers from the given image using Tesseract OCR.

    :param image_path: Path to the image file
    :param preprocess: Boolean flag to apply OpenCV preprocessing
    :return: Extracted text as a string
    """
    try:
        if preprocess:
            # Open the image with OpenCV
            image = cv2.imread(image_path)

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply binarization (Thresholding) to enhance readability
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Save the processed image
            output_image_path = os.path.join('outputs', 'preprocess_img.png')
            cv2.imwrite(output_image_path, binary)

            print(f"Processed image saved to: {output_image_path}")

            # Convert processed image to a format compatible with Pillow
            processed_image = Image.fromarray(binary)
        else:
            # Open image directly without preprocessing
            processed_image = Image.open(image_path)

        # Tesseract configuration (no whitelist or blacklist, allowing all characters)
        custom_config = "--oem 3 --psm 6"

        # Extract text with OCR
        text = pytesseract.image_to_string(processed_image, config=custom_config)

        return text.strip()
    except Exception as e:
        return f"Error: {e}"
