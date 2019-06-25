def pre_processing(image):
    #h, w = image.shape[:2]
    #image = cv2.resize(image, (int(w/2), int(h/2)))
    h, w = image.shape[:2]
    """for i in range(0, h):
        for j in range(0, w):
            if image[i][j][0] <= 30 and image[i][j][1] <= 30 and image[i][j][2] <= 30:
                image[i][j] = 0,0,0
            elif image[i][j][0] >= 230 and image[i][j][1] >= 230 and image[i][j][2] >= 230:
                image[i][j] = 255,255,255"""
    return image