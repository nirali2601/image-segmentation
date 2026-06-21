# image-segmentation-tool

A small example project that runs Mask R-CNN image segmentation using PyTorch and OpenCV.

## Overview

This repository provides a minimal tool to run instance segmentation on a single image using a pre-trained Mask R-CNN model from `torchvision`.

Key files:
- [main.py](main.py#L1-L40): CLI entrypoint that loads the image, runs segmentation, and saves/displays the result.
- [model.py](model.py#L1-L200): Loads the Mask R-CNN model and runs inference.
- [utils.py](utils.py#L1-L200): Image loading and visualization helpers.
- [requirements.txt](requirements.txt#L1-L4): Python dependencies.

## Requirements

- Python 3.8+ (3.11 recommended)
- Pip
- Optional: CUDA-enabled GPU for faster inference (PyTorch with CUDA)

The Python packages required are listed in [requirements.txt](requirements.txt#L1-L4).

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

## Running the tool

The CLI entrypoint is [main.py](main.py#L1-L40). Basic usage:

```powershell
# Run with defaults (looks for image2.jpg in the repo root)
python main.py

# Specify input image, output path, and confidence threshold
python main.py --input path\to\image.jpg --output result.jpg --threshold 0.6
```

Behavior:
- On first run the torchvision pretrained weights will be downloaded automatically (internet required).
- If CUDA is available the model and input tensors are moved to GPU.
- The script writes the segmented output image and also opens an OpenCV window (`cv2.imshow`) to display results. You can close the window to exit.

## Example

Place an image named `image2.jpg` in the repository root and run:

```powershell
python main.py --output output2.jpg
```

Output will be saved to `output2.jpg` and displayed on-screen.

## Troubleshooting

- If OpenCV window doesn't appear or errors happen when running in a headless environment (e.g., remote server), remove or comment out the `cv2.imshow`, `cv2.waitKey`, and `cv2.destroyAllWindows()` calls in `main.py`.
- If dependency installation fails for `torch`/`torchvision`, follow the official installation instructions at https://pytorch.org/ for your OS and CUDA version.
- If images fail to load, ensure the input path is correct and supported by OpenCV.

## License

This project is provided as an example; adapt and reuse as you wish.
