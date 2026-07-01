import cv2
import argparse
import os
import sys
from io import BytesIO
import base64
from flask import Flask, request, jsonify
import numpy as np
from model import load_mask_rcnn, segment_image
from utils import load_image, visualize_segmentation

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Load model once at startup
model = None

def load_model():
    """Load the Mask R-CNN model once at startup"""
    global model
    if model is None:
        model = load_mask_rcnn()
    return model

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Image Segmentation API is running'}), 200

@app.route('/segment', methods=['POST'])
def segment():
    """
    Segment an uploaded image
    
    Expected form data:
    - 'image': Image file (JPG, PNG, BMP, etc.)
    - 'threshold': Confidence threshold (0.0-1.0, default: 0.5)
    
    Returns:
    - JSON with segmented image as base64-encoded string
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Get confidence threshold
        threshold = request.form.get('threshold', default=0.5, type=float)
        if not (0.0 <= threshold <= 1.0):
            return jsonify({'error': 'Threshold must be between 0.0 and 1.0'}), 400
        
        # Read image file
        image_data = image_file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Load model if not already loaded
        model = load_model()
        
        # Perform segmentation
        predictions = segment_image(model, img, threshold)
        
        # Visualize results
        output_img = visualize_segmentation(img, predictions)
        
        # Convert output image to base64
        output_bgr = cv2.cvtColor(output_img.astype(np.uint8), cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', output_bgr)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'image': image_base64,
            'detections': len(predictions['boxes']),
            'threshold': threshold
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Segmentation failed: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'service': 'Image Segmentation API',
        'version': '1.0',
        'endpoints': {
            'GET /health': 'Health check',
            'POST /segment': 'Upload image for segmentation (form data: image, threshold)'
        },
        'usage': {
            'example': 'curl -F "image=@image.jpg" -F "threshold=0.5" http://localhost:5000/segment'
        }
    }), 200

@app.before_request
def before_request():
    """Load model on first request"""
    load_model()

def run_cli():
    """CLI mode for local testing"""
    parser = argparse.ArgumentParser(description="Image Segmentation Tool")
    parser.add_argument('--input', type=str, default='image2.jpg', help='Path to input image')
    parser.add_argument('--output', type=str, default='output2.jpg', help='Path to output image')
    parser.add_argument('--threshold', type=float, default=0.5, help='Confidence threshold for detection')
    # Parse arguments starting from index 2 to skip 'main.py' and '--cli'
    args = parser.parse_args(sys.argv[2:])

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
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        run_cli()
    else:
        app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))