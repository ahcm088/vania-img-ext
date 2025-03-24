import os
import cv2
import easyocr
import numpy as np
from sklearn.cluster import DBSCAN

def ensure_directory(directory):
    """Ensure the directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def preprocess_image(image_path):
    """Apply adaptive thresholding for better text detection."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return binary

def group_text_boxes(results, original_image, save_dir="outputs/cropped_texts/", eps=50, min_samples=1):
    """Group bounding boxes using DBSCAN clustering with more loose proximity to reconstruct text order."""
    if not results:
        return []

    ensure_directory(save_dir)

    # Extract bounding boxes, text, and centers
    boxes = [bbox for bbox, _, _ in results]
    texts = [text for _, text, _ in results]
    centers = [(int((bbox[0][0] + bbox[2][0]) / 2), int((bbox[0][1] + bbox[2][1]) / 2)) for bbox in boxes]

    # Convert to NumPy array for clustering
    centers_array = np.array(centers)

    # Apply DBSCAN clustering with a larger eps to group nearby blocks
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean').fit(centers_array)

    grouped_texts = {}
    for i, (label, bbox, text) in enumerate(zip(clustering.labels_, boxes, texts)):
        if label not in grouped_texts:
            grouped_texts[label] = []
        grouped_texts[label].append(text)

        # Extract bounding box coordinates
        x_min, y_min = int(bbox[0][0]), int(bbox[0][1])
        x_max, y_max = int(bbox[2][0]), int(bbox[2][1])

        # Save cropped text region
        cropped_region = original_image[y_min:y_max, x_min:x_max]
        crop_filename = os.path.join(save_dir, f"text_region_{i}.png")
        cv2.imwrite(crop_filename, cropped_region)

        # Draw bounding box on the image
        cv2.rectangle(original_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Save the image with bounding boxes
    detected_image_path = os.path.join(save_dir, "detected_text.png")
    cv2.imwrite(detected_image_path, original_image)

    # Sort clusters by vertical position and merge texts
    sorted_clusters = sorted(grouped_texts.items(), key=lambda x: min(centers[i][1] for i, lbl in enumerate(clustering.labels_) if lbl == x[0]))

    # Prepare the output to print in a more readable format
    formatted_output = []
    for label, texts in sorted_clusters:
        cluster_content = "\n    ".join(texts)
        formatted_output.append(f"Cluster {label}:\n    {cluster_content}")

    # Return the formatted output as a single string
    return "\n\n".join(formatted_output)

def extract_text_with_grouping(image_path, eps=50):
    """Extract and group text using bounding boxes and clustering with more flexible proximity."""
    try:
        processed_image = preprocess_image(image_path)
        original_image = cv2.imread(image_path)  # Load original image to save cropped regions
        reader = easyocr.Reader(['pt'])
        results = reader.readtext(processed_image)

        if not results:
            return "No text detected."

        # Group text boxes and save images
        grouped_text = group_text_boxes(results, original_image, eps=eps)

        return grouped_text  # Return formatted grouped text
    except Exception as e:
        return f"Error: {e}"
