import argparse
from ocr_module import extract_text_with_grouping

def main():
    parser = argparse.ArgumentParser(description="Extract text from an image using optional preprocessing, adaptive thresholding, and bounding boxes.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("--no-preprocess", action="store_true", help="Disable image preprocessing.")
    parser.add_argument("--eps", type=float, default=50, help="Epsilon value for DBSCAN clustering (default: 50).")
    
    args = parser.parse_args()
    
    # Run OCR with optional preprocessing, adaptive thresholding, bounding boxes, and adjustable eps
    extracted_text = extract_text_with_grouping(args.image_path, preprocess=not args.no_preprocess, eps=args.eps)
    
    print("Extracted Text:\n", extracted_text)

if __name__ == "__main__":
    main()
