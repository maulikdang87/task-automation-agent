from TaskB.task_b12 import B12
from PIL import Image

def B7(image_path, output_path, resize=None):
    
    if not B12(image_path):
        return None
    if not B12(output_path):
        return None
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)