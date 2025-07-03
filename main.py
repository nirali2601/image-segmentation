import cv2
import argparse
from model import load_mask_rcnn, segment_image
from utils import load_image, visualize_segmentation

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Image Segmentation Tool")
    parser.add_argument('--input', type=str, default='image2.jpg', help='Path to input image')
    parser.add_argument('--output', type=str, default='output2.jpg', help='Path to output image')
    parser.add_argument('--threshold', type=float, default=0.5, help='Confidence threshold for detection')
    args = parser.parse_args()

    # Load image
    img = load_image(args.input)
    if img is None:
        print(f"Error: Could not load image at {args.input}")
        return

    # Load model
    model = load_mask_rcnn()

    # Perform segmentation
    predictions = segment_image(model, img, args.threshold)

    # Visualize results
    output_img = visualize_segmentation(img, predictions)

    # Save and display output
    cv2.imwrite(args.output, cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
    print(f"Output saved to {args.output}")
    cv2.imshow('Segmented Image', cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()