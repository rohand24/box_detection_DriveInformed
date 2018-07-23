Box Detection
=============

This code is for detecting boxes in any scanned document image.
This code uses thresholding , windowing and morphological operations to preprocess the image and 
then use contour detection to detect rectangular contours and use this to highlight boxes in the original image.
The points from the detected rectangular contours are written to a json file.

To Run the Code:

- Clone this git repo to a directory.
- cd <to cloned directory>
- python detect.py --input_path <path to input images. default = './examples/inputs'> --output_path <path to output images. default = './output'>


Libraries used:

- OpenCV
- numpy
- json
- glob2

Files:

1] 'detect.py' : This is the file used to detect the boxes and save it to the output path and save the points to json file.
2] 'helper.py' : This file consists of all the helper functions required for preprocessing the image.

Process:

1] Windowing : The image is cropped into windows for edge detection. Also, for efficiently detecting both, small and large edges,
two windows, namely 'small_win_mask' and 'large_win_mask' are used.

2] Thresholding : Every window of the image is gaussian filtered and then thresholded using opencv's 'Adaptive Gaussian Thresholding' technique.
Then the thresholded window image is passed to morphological operations.
    
3] Morphological operations : Uses horizontal and vertical kernels to detect horizontal and vertical lines using OpenCV's 'dilate' and 'erode' methods.
The horizontal and vertical line masks are added to form a mask that contains boxes.

4] Contour detection : This is done using OpenCV's 'findContours' method. The approx contour is calculated using 'arcLength' and 'approxPolyDP' methods. 
Using this approx contour, shape of the contour is detected and if it is rectangular, it is drawn on the original image using 'drawContour' method and
its points are written to json file in required format.



