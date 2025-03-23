import os
import cv2
import easyocr
import matplotlib.pyplot as plt

def ensure_directory(directory):
    """Ensure the directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_user_window_size(image_path, initial_size):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return initial_size
    
    height, width = image.shape[:2]
    while True:
        window_width, window_height = initial_size
        cropped = image[0:window_height, 0:window_width]
        cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        plt.imshow(cropped_rgb)
        plt.title(f"Window Size: {window_width}x{window_height}")
        plt.axis("off")
        plt.show()
        user_input = input(f"Current window size: {window_width}x{window_height}. Keep it? (y/n): ").strip().lower()
        if user_input == "y":
            return (window_width, window_height)
        elif user_input == "n":
            try:
                window_width = int(input("Enter new width: "))
                window_height = int(input("Enter new height: "))
                initial_size = (window_width, window_height)
            except ValueError:
                print("Invalid input. Please enter numeric values.")
        else:
            print("Invalid option. Type 'y' to confirm or 'n' to modify the window size.")

def extract_text_with_window(image_path, window_size=(100, 100), preprocess=False):
    try:
        image = cv2.imread(image_path)
        if preprocess:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            processed_image = binary
        else:
            processed_image = image
        
        reader = easyocr.Reader(['pt'])
        height, width = processed_image.shape[:2]
        window_width, window_height = window_size
        extracted_text = []
        save_dir = "outputs/subfigs"
        ensure_directory(save_dir)
        
        for y in range(0, height - window_height + 1, window_height):
            for x in range(0, width - window_width + 1, window_width):
                window = processed_image[y:y + window_height, x:x + window_width]
                window_filename = os.path.join(save_dir, f"window_{x}_{y}.png")
                cv2.imwrite(window_filename, window)
                result = reader.readtext(window)
                window_text = ' '.join([item[1] for item in result]).strip()
                if window_text:
                    extracted_text.append(f"Window ({x}, {y}) - ({x + window_width}, {y + window_height}):\n{window_text}\n")
        return '\n'.join(extracted_text)
    except Exception as e:
        return f"Error: {e}"
