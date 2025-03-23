import os
from PIL import Image
import pytesseract
import cv2

def extract_text(image_path, preprocess=False):
    """
    Extract text including numbers from the given image using Tesseract OCR.

    :param image_path: Path to the image file
    :param preprocess: Boolean flag to apply OpenCV preprocessing
    :return: Extracted text as a formatted string
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

        # Format the extracted text
        formatted_text = format_text(text)

        return formatted_text
    except Exception as e:
        return f"Error: {e}"

def format_text(text):
    """
    Format the extracted text into a more readable format.

    :param text: Extracted text as a string
    :return: Formatted text as a string
    """
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')

    # Format each paragraph
    formatted_paragraphs = []
    for paragraph in paragraphs:
        # Split the paragraph into lines
        lines = paragraph.split('\n')
        # Remove empty lines and strip whitespace
        lines = [line.strip() for line in lines if line.strip()]
        # Join lines with a single newline character
        formatted_paragraph = '\n'.join(lines)
        # Add the formatted paragraph to the list
        formatted_paragraphs.append(formatted_paragraph)

    # Join paragraphs with double newline characters
    formatted_text = '\n\n'.join(formatted_paragraphs)

    return formatted_text
