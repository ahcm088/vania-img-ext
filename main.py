import argparse
from ocr_module import extract_text_with_window, get_user_window_size

def main():
    parser = argparse.ArgumentParser(description="Extract text and numbers from an image using a sliding window.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("--window_size", type=int, nargs=2, metavar=("WIDTH", "HEIGHT"), default=(100, 100),
                        help="Size of the sliding window as two integers: width height (default: 100 100).")
    parser.add_argument("--preprocess", action="store_true", help="Enable image preprocessing with OpenCV.")

    args = parser.parse_args()

    # Let the user adjust the window size interactively
    final_window_size = get_user_window_size(args.image_path, tuple(args.window_size))

    # Run OCR with the selected window size
    extracted_text = extract_text_with_window(args.image_path, final_window_size, args.preprocess)

    print("Extracted Text:\n", extracted_text)

if __name__ == "__main__":
    main()
