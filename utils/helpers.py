from PIL import Image

def get_image_size(image):
    return image.size  # returns (width, height)

def read_annotation_file(file):
    return file.read().decode("utf-8")
