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

The application provides both a web API and CLI mode.

### Web API (Default)

Start the web server:

```bash
python main.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

**GET `/`** - API documentation
```bash
curl http://localhost:5000/
```

**GET `/health`** - Health check
```bash
curl http://localhost:5000/health
```

**POST `/segment`** - Perform image segmentation
```bash
curl -F "image=@image.jpg" -F "threshold=0.5" http://localhost:5000/segment
```

**Parameters:**
- `image` (required): Image file (JPG, PNG, BMP, etc.)
- `threshold` (optional): Confidence threshold for detections (0.0-1.0, default: 0.5)

**Response:**
```json
{
  "status": "success",
  "image": "base64_encoded_image_string",
  "detections": 5,
  "threshold": 0.5
}
```

### CLI Mode (Local Testing)

For command-line usage:

```bash
python main.py --cli --input path/to/image.jpg --output result.jpg --threshold 0.6
```

**Arguments:**
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

## Deployment

### ⚠️ Important: Vercel Limitations
**Note:** Vercel has a 250MB size limit for Python deployments. PyTorch + TorchVision can exceed this limit. If you encounter deployment issues, use **Render** or **Railway** instead (recommended alternatives).

### Vercel Deployment (Recommended for Learning)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy to Vercel:**
   ```bash
   vercel
   ```

3. **Follow the prompts:**
   - Link your Git repository
   - Confirm project settings
   - Deploy

4. **Your app will be live at:** `https://your-project.vercel.app`

**Test the API:**
```bash
curl https://your-project.vercel.app/health
curl -F "image=@image.jpg" https://your-project.vercel.app/segment
```

### Railway Deployment (Recommended Alternative)

Railway works better with Python ML applications due to higher resource limits.

1. **Create account at [railway.app](https://railway.app)**

2. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

3. **Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

### Render Deployment (Another Great Alternative)

1. **Create account at [render.com](https://render.com)**

2. **Create a new Web Service:**
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn main:app`
   - Choose appropriate plan

3. **Deploy and your app will be live!**

### Heroku Deployment (Still Available)

1. Install the Heroku CLI
2. Log in to Heroku:
   ```bash
   heroku login
   ```

3. Create a Heroku app:
   ```bash
   heroku create your-app-name
   ```

4. Push to Heroku:
   ```bash
   git push heroku main
   ```

5. Check the application:
   ```bash
   heroku logs --tail
   heroku open
   ```

The app will be available at `https://your-app-name.herokuapp.com`

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web server
python main.py

# Test the API
curl http://localhost:5000/health
curl -F "image=@image.jpg" http://localhost:5000/segment
```

### Docker Deployment

You can also containerize the application for deployment to AWS, Google Cloud, Azure, or any Docker-compatible platform.

```bash
docker build -t image-segmentation .
docker run -p 5000:5000 image-segmentation
```

## Environment Variables

- `PORT` - Server port (default: 5000)
- `FLASK_ENV` - Environment mode (default: production)



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


cd d:\Downloads\project-2\image-segmentation-tool
.\segmentation-env\Scripts\Activate.ps1

# Run with your image
python main.py --cli --input input.jpeg --output output_result.jpg

# image-segmentation
