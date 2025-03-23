import os
from PIL import Image
import cv2
import easyocr

def extract_text(image_path, preprocess=False):
    """
    Extract text including numbers from the given image using EasyOCR.

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

            # The binary image is already a NumPy array, no need to convert to Pillow format
            processed_image = binary
        else:
            # Open image directly with OpenCV (as a NumPy array)
            processed_image = cv2.imread(image_path)

        # Initialize EasyOCR reader with Portuguese language
        reader = easyocr.Reader(['pt'])  # 'pt' is the code for Portuguese

        # Extract text with OCR using EasyOCR
        result = reader.readtext(processed_image)

        # Create formatted text by joining text within each detected line
        formatted_text = ''
        current_line = []

        for item in result:
            text = item[1]
            # If the text is separated by a reasonable amount of space (line break)
            # we assume it's a new line, otherwise we continue on the same line.
            if len(current_line) == 0 or abs(item[0][0][1] - item[0][2][1]) < 15:  # Compare Y positions
                current_line.append(text)
            else:
                formatted_text += ' '.join(current_line) + '\n'
                current_line = [text]

        # Add the last line if there is one
        if current_line:
            formatted_text += ' '.join(current_line)

        return formatted_text.strip()

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
