# Image Segmentation Tool

A Python tool that performs instance segmentation on images using a pre-trained Mask R-CNN model from PyTorch and OpenCV.

## Overview

This repository provides a minimal command-line tool to run instance segmentation on images using a pre-trained Mask R-CNN model from `torchvision`.

### Key Features
- Pre-trained Mask R-CNN model (ResNet-50 FPN backbone)
- GPU acceleration support (CUDA)
- Command-line interface for easy usage
- Confidence threshold filtering
- Real-time visualization

### Project Structure
- [main.py](main.py) - CLI entrypoint that loads images, runs segmentation, and saves/displays results
- [model.py](model.py) - Mask R-CNN model loading and inference
- [utils.py](utils.py) - Image loading and visualization utilities
- [requirements.txt](requirements.txt) - Python package dependencies

## Requirements

- Python 3.8+ (3.11 recommended)
- pip package manager
- Optional: CUDA-enabled GPU for faster inference

### Python Dependencies
All required packages are listed in [requirements.txt](requirements.txt):
- OpenCV (cv2)
- PyTorch
- TorchVision
- NumPy

## Setup (Windows)

You can either use the provided virtual environment or create a fresh one.

Using the included venv (already present in this repo):

PowerShell:

```powershell
.\segmentation-env\Scripts\Activate.ps1
```

CMD:

```cmd
.\segmentation-env\Scripts\activate.bat
```

Or create and use a new venv:

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

CMD:

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

## Install dependencies

After activating your venv, run:

```powershell
pip install -r requirements.txt
```

Notes:
- Installing `torch`/`torchvision` may pick CPU-only or CUDA builds depending on your platform and pip configuration. If you need a specific CUDA build, follow the instructions at https://pytorch.org/ and install the appropriate packages before running the script.

## Usage

The main entry point is [main.py](main.py). Basic usage:

```bash
# Run with defaults (looks for image2.jpg in the current directory)
python main.py

# Specify custom input image, output path, and confidence threshold
python main.py --input path/to/image.jpg --output result.jpg --threshold 0.6
```

### Command-Line Arguments
- `--input` - Path to input image (default: `image2.jpg`)
- `--output` - Path to save output image (default: `output2.jpg`)
- `--threshold` - Confidence threshold for detections (default: `0.5`, range: `0.0-1.0`)

### How It Works
1. Loads pre-trained Mask R-CNN weights (downloaded automatically on first run - requires internet)
2. Reads the input image using OpenCV
3. Converts image to PyTorch tensor format
4. Runs inference on GPU (if available) or CPU
5. Filters predictions by confidence threshold
6. Overlays segmentation masks and bounding boxes
7. Saves the output image and displays it in an OpenCV window

## Quick Start Example

1. Place an image named `image2.jpg` in the repository root directory
2. Run the segmentation:
   ```bash
   python main.py --output output2.jpg
   ```
3. The segmented image will be saved as `output2.jpg` and displayed on-screen
4. Press any key in the OpenCV window to exit

## Troubleshooting

### OpenCV Window Not Displaying
If running in a headless environment (e.g., remote server), comment out these lines in `main.py`:
```python
cv2.imshow('Segmented Image', cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Dependency Installation Issues
If `torch` or `torchvision` installation fails:
1. Visit [pytorch.org](https://pytorch.org/)
2. Select your OS and CUDA version
3. Install the recommended packages before running `pip install -r requirements.txt`

### Image Loading Failures
- Verify the image file path is correct
- Ensure the image format is supported by OpenCV (JPG, PNG, BMP, etc.)
- Try using an absolute path instead of a relative path

## License

This project is provided as-is for educational and research purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
