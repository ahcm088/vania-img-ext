import argparse
from ocr_module import extract_text

def main():
    parser = argparse.ArgumentParser(description="Extract text and numbers from an image.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("--preprocess", action="store_true", help="Enable image preprocessing with OpenCV.")

    args = parser.parse_args()

    extracted_text = extract_text(args.image_path, args.preprocess)
    print("Extracted Text:\n", extracted_text)

if __name__ == "__main__":
    main()
