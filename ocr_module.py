import os
import cv2
import easyocr
import numpy as np
import argparse
from sklearn.cluster import DBSCAN

def ensure_directory(directory):
    """Ensure the directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def preprocess_image(image_path):
    """Apply image preprocessing techniques for better OCR accuracy."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Denoising to remove small noise
    denoised = cv2.fastNlMeansDenoising(image, h=30)
    
    # Improve contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    # Adaptive Thresholding for binarization
    binary = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Morphological operations to remove small white noise
    kernel = np.ones((2,2), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return cleaned

def draw_bounding_boxes(image, results, save_path):
    """Draw bounding boxes on an image and save it."""
    for bbox, _, _ in results:
        x_min, y_min = int(bbox[0][0]), int(bbox[0][1])
        x_max, y_max = int(bbox[2][0]), int(bbox[2][1])
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    
    cv2.imwrite(save_path, image)

def group_text_boxes(results, original_image, preprocessed_image=None, save_dir="outputs/cropped_texts/", eps=50, min_samples=1):
    """Group bounding boxes using DBSCAN clustering to reconstruct text order."""
    if not results:
        return []

    ensure_directory(save_dir)
    
    boxes = [bbox for bbox, _, _ in results]
    texts = [text for _, text, _ in results]
    centers = [(int((bbox[0][0] + bbox[2][0]) / 2), int((bbox[0][1] + bbox[2][1]) / 2)) for bbox in boxes]
    
    centers_array = np.array(centers)
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean').fit(centers_array)
    
    grouped_texts = {}
    for i, (label, bbox, text) in enumerate(zip(clustering.labels_, boxes, texts)):
        if label not in grouped_texts:
            grouped_texts[label] = []
        grouped_texts[label].append(text)
        
        x_min, y_min = int(bbox[0][0]), int(bbox[0][1])
        x_max, y_max = int(bbox[2][0]), int(bbox[2][1])
        
        # Save cropped region from the appropriate image (preprocessed if used, original if not)
        if text.strip():  # Only save regions with detected text
            cropped_region = preprocessed_image[y_min:y_max, x_min:x_max] if preprocessed_image is not None else original_image[y_min:y_max, x_min:x_max]
            crop_filename = os.path.join(save_dir, f"text_region_{i}.png")
            cv2.imwrite(crop_filename, cropped_region)
        
        # Draw bounding boxes on the original image
        cv2.rectangle(original_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        
        if preprocessed_image is not None:
            # Draw bounding boxes on the preprocessed image
            cv2.rectangle(preprocessed_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Save images with bounding boxes if OCR results are found
    if any(text.strip() for _, text, _ in results):
        cv2.imwrite(os.path.join(save_dir, "detected_text_original.png"), original_image)
    
    if preprocessed_image is not None and any(text.strip() for _, text, _ in results):
        cv2.imwrite(os.path.join(save_dir, "detected_text_preprocessed.png"), preprocessed_image)

    sorted_clusters = sorted(grouped_texts.items(), key=lambda x: min(centers[i][1] for i, lbl in enumerate(clustering.labels_) if lbl == x[0]))
    
    formatted_output = []
    for label, texts in sorted_clusters:
        cluster_content = "\n    ".join(texts)
        formatted_output.append(f"Cluster {label}:\n    {cluster_content}")
    
    return "\n\n".join(formatted_output)

def extract_text_with_grouping(image_path, preprocess=True, eps=50):
    """Extract and group text using bounding boxes and clustering."""
    try:
        if preprocess:
            processed_image = preprocess_image(image_path)
            preprocessed_image_color = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)  # Convert for bounding box drawing
        else:
            processed_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            preprocessed_image_color = None

        original_image = cv2.imread(image_path)
        reader = easyocr.Reader(['pt'])
        results = reader.readtext(processed_image)

        if not results:
            return "No text detected."

        grouped_text = group_text_boxes(results, original_image, preprocessed_image_color, eps=eps)
        
        return grouped_text
    except Exception as e:
        return f"Error: {e}"
