import cv2
import numpy as np
import random

# COCO class names (subset for simplicity; full list has 80 classes)
COCO_CLASSES = [
    'background', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
    'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe'
]

def load_image(image_path):
    """
    Load an image using OpenCV and convert to RGB.
    Args:
        image_path: Path to the input image.
    Returns:
        img: Image as numpy array in RGB format, or None if loading fails.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def visualize_segmentation(img, predictions):
    """
    Visualize segmentation results by overlaying masks and bounding boxes.
    Args:
        img: Input image as numpy array (RGB).
        predictions: Dictionary with boxes, labels, scores, and masks.
    Returns:
        output_img: Image with overlaid masks and bounding boxes.
    """
    output_img = img.copy()
    for i in range(len(predictions['boxes'])):
        # Get prediction details
        box = predictions['boxes'][i].astype(int)
        label = predictions['labels'][i]
        score = predictions['scores'][i]
        mask = predictions['masks'][i, 0] > 0.5  # Threshold mask

        # Generate random color for mask
        color = [random.randint(0, 255) for _ in range(3)]
        output_img[mask] = output_img[mask] * 0.5 + np.array(color) * 0.5

        # Draw bounding box
        cv2.rectangle(output_img, (box[0], box[1]), (box[2], box[3]), color, 2)

        # Add label and score
        label_text = f"{COCO_CLASSES[label] if label < len(COCO_CLASSES) else 'unknown'}: {score:.2f}"
        cv2.putText(output_img, label_text, (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return output_img