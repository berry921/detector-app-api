import cv2
import numpy as np
import PIL


def load_image(image, scale):
    _bytes = np.frombuffer(image.read(), np.uint8)
    original_np_image = cv2.imdecode(_bytes, flags=cv2.IMREAD_COLOR)
    np_image = cv2.cvtColor(original_np_image, cv2.COLOR_BGR2RGB)
    # Create image object
    image_obj = PIL.Image.fromarray(np_image)
    ratio = image_obj.size[1] / image_obj.size[0]  # Image aspect ratio
    if ratio >= 1.0:  # If the image is vertical
        reshaped_size = (int((1 / ratio) * scale), scale)
    else:  # If the image is landscape
        reshaped_size = (scale, int(ratio * scale))
    print(reshaped_size)
    # resize image
    image = image_obj.resize(reshaped_size)
    return image
