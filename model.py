import torch
import torchvision.transforms as T
from torchvision.models.detection import maskrcnn_resnet50_fpn

def load_mask_rcnn():
    """
    Load pre-trained Mask R-CNN model from PyTorch Hub.
    Returns:
        model: Pre-trained Mask R-CNN model in evaluation mode.
    """
    model = maskrcnn_resnet50_fpn(weights='DEFAULT')
    model.eval()  # Set to evaluation mode
    if torch.cuda.is_available():
        model = model.cuda()
    return model

def segment_image(model, img, confidence_threshold=0.5):
    """
    Run segmentation on the input image.
    Args:
        model: Pre-trained Mask R-CNN model.
        img: Input image as numpy array (H, W, C) in RGB format.
        confidence_threshold: Minimum confidence score for detections.
    Returns:
        predictions: Dictionary containing boxes, labels, scores, and masks.
    """
    # Convert image to tensor
    transform = T.ToTensor()
    img_tensor = transform(img)
    if torch.cuda.is_available():
        img_tensor = img_tensor.cuda()

    # Add batch dimension
    img_tensor = img_tensor.unsqueeze(0)

    # Run inference
    with torch.no_grad():
        predictions = model(img_tensor)[0]

    # Filter predictions by confidence threshold
    mask = predictions['scores'] > confidence_threshold
    filtered_predictions = {
        'boxes': predictions['boxes'][mask].cpu().numpy(),
        'labels': predictions['labels'][mask].cpu().numpy(),
        'scores': predictions['scores'][mask].cpu().numpy(),
        'masks': predictions['masks'][mask].cpu().numpy()
    }
    return filtered_predictions