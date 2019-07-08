import cv2
def resize(image):
    h, w = image.shape[:2]
    if w > 1600:
        resized = cv2.resize(image, (int(w / 4), int(h / 4)), interpolation=cv2.INTER_AREA)
        return resized
    return image