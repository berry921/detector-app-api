import numpy as np
import cv2
import PIL


def load_image(image, scale):
    """画像の読み込み"""
    _bytes = np.frombuffer(image.read(), np.uint8)
    original_np_image = cv2.imdecode(_bytes, flags=cv2.IMREAD_COLOR)
    np_image = cv2.cvtColor(original_np_image, cv2.COLOR_BGR2RGB)
    # 画像データのオブジェクトを作成
    image_obj = PIL.Image.fromarray(np_image)
    ratio = (image_obj.size[1] / image_obj.size[0])  # 画像の縦横比
    if ratio >= 1.0:  # 画像が縦長である場合
        reshaped_size = (int((1/ratio)*scale), scale)
    else:  # 画像が横長である場合
        reshaped_size = (scale, int(ratio*scale))
    print(reshaped_size)
    # 画像データのサイズ変更
    image = image_obj.resize(reshaped_size)
    return image
