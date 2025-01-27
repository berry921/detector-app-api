import torchvision


def image_to_tensor(image):
    """Convert an image to tensor data type"""
    image_tensor = torchvision.transforms.functional.to_tensor(image)
    return image_tensor
