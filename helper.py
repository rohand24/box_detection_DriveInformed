import cv2

# function to get window from an image
def get_window(img,step_size,win_size):

    for x in range(0,img.shape[0],step_size):
       for y in range(0,img.shape[1],step_size):
           yield (x,y,img[y:y+win_size[1], x:x+win_size[0]])

# function to get different types of Thresholding
def threshold(src, type):

    if type == 'adaptive':
        th = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                               cv2.THRESH_BINARY, 75, 10)
    if type == 'binary':
        ret, th = cv2.threshold(src, 127, 255,cv2.THRESH_BINARY)
    if type == 'otsu':
        ret, th = cv2.threshold(src, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if type == 'adaptive_gaussian':
        th = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                   cv2.THRESH_BINARY, 75, 10)

    return th

# function to get different kernels for morphological ops
def get_kernel(type,tup):

    if type == 'rect':
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, tup)
    if type == 'cross':
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, tup)
    if type == 'ellipse':
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, tup)
    return kernel

# function to perform morphological ops (erosion, dilation)
def morphological_ops(src, kernel, eroded = 1, dilated = 1):

    if eroded and not dilated :
        src = cv2.erode(src, kernel, iterations=1)
        return src
    elif dilated and not eroded:
        src = cv2.dilate(src, kernel, iterations=1)
        return src
    elif eroded and dilated:
        src = cv2.erode(src, kernel, iterations=1)
        src = cv2.dilate(src, kernel, iterations=1)
        return src

# function to resize the image
def resize(img, height=500):

    ratio = height/img.shape[0]
    return cv2.resize(img,(int(ratio*img.shape[1]), height))


# Function to filter the image and remove noise
def smoothen(src,type,ksize):

    if type == 'median':
        blur = cv2.medianBlur(src, 3, None)
    if type == 'gaussian':
        blur = cv2.GaussianBlur(src, ksize, 0)
    if type == 'bilateral':
        blur = cv2.bilateralFilter(src,ksize,75,75)
    return blur

# Function to read image and convert it to grayscale
def read_img(fname):
    c_img = cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(c_img, cv2.COLOR_RGB2GRAY)

    return gray_img, c_img