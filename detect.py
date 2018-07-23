import os
import numpy as np
import cv2
import argparse
import glob2
import matplotlib.pyplot as plt
import pdb
import json
from helper import *

def parse_args():
# Function to parse arguments
    parser = argparse.ArgumentParser(description='Process input arguments.')
    parser.add_argument('input_path', default='./examples/inputs', help = 'Path to input files')
    parser.add_argument('output_path', default='./output', help = 'Path to output directory to store output files.')

    args = parser.parse_args()

    return args

def get_canny(img):

# Function to detect edges using canny edge detector.
# Unused
    img = smoothen(img, 'gaussian', (7,7))
    img = threshold(img, 'adaptive')
    img = smoothen(img, 'median', 3)

    edges = cv2.Canny(img, 10, 250)
    edges1 = smoothen(edges, 'bilateral', 7)
    edges1 = smoothen(edges1, 'median', 3)
    edges1 = get_mask(edges1)

    edges = edges - edges1

    return edges


def morphological_process(img, ktype, kh, kv):
# Perform morphological ops using horizontal and vertical kernels
    horizontal_img = img.copy()
    vertical_img = img.copy()

    kernel = get_kernel(ktype, (kh, 1))
    horizontal_img = morphological_ops(horizontal_img, kernel, 1, 1)
    kernel = get_kernel(ktype, (1, kv))
    vertical_img = morphological_ops(vertical_img, kernel, 1, 1)

    mask = horizontal_img + vertical_img

    return mask


def get_mask(img):

# Image preprocessing
# Gaussian filtering and thresholding to detect sharp edges.
# Invert image to remove noise.
    img = smoothen(img, 'gaussian', (5,5))
    img = cv2.addWeighted(img, 1.5, img, -0.5, 0)  # sharpen edges
    thresh_img = threshold(img, 'adaptive_gaussian')
    inv = 255 - thresh_img

    mask_img = morphological_process(inv, 'rect', 15,15)

    return mask_img


def windowing(img, win_size, step_size):
# This function divides the image into windows, performs morphological ops
# on each window and stores it in a mask. The mask image is returned.
    mask = np.zeros_like(img)
    for (x,y,window) in get_window(img, step_size, win_size):
        if window.shape[0] <= 0.01*(win_size[0]) or window.shape[1] <= 0.01*(win_size[1]):
            continue
        win_mask = get_mask(window)
        mask[y:y+win_size[1],x:x+win_size[0]] = win_mask

# Extra morphological ops to detect edges better.
    mask = morphological_process(mask, 'rect', 35,35)
    mask= smoothen(mask,'median',5)

    return mask

def detect_box(image, output_path):

    fname = image.split('\\')[-1].split('.')[0] #
    gray_img, c_img = read_img(image) # read image

# Define constants
    small_win_size = [50,50]
    small_step_size = 10
    big_win_size = [int(c_img.shape[1]/2),int(c_img.shape[0]/2)]
    big_step_size = 100

# Get mask using 2 windows
    small_win_mask = windowing(gray_img, small_win_size,small_step_size)
    big_win_mask = windowing(gray_img, big_win_size, big_step_size)
    mask = small_win_mask+big_win_mask

# Get contours and find rectangle boxes
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    json_dict = {}
    rects=[]
    boxes = []
    for c in contours:
        peri = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,0.015*peri, True)

        if len(approx)>=3 and len(approx)<=6:
            rects.append(c) # append all rectangle boxes

            # Add points of each box to the dictonary
            box = []
            middle = {}
            for i in range(len(c)):
                box.append(c[i][0].tolist())
            middle['points'] = box
            boxes.append(middle)
    json_dict['boxes'] = boxes
    cv2.drawContours(c_img, rects, -1, (0, 0, 255), 3)

    # Save the image with contours drawn on it
    cv2.imwrite(output_path+'/'+fname + '_output.jpg', c_img)
    # cv2.imwrite(output_path+'/'+fname+'_mask.jpg', mask)

    # Write the dictionary to json file
    with open(output_path+'/'+fname + '_points.json', 'w+') as f:
        json.dump(json_dict,f)


def read_data(input_path):

    all_files = glob2.glob(input_path+ '/*.jpg')

    return all_files

def main():

    args = parse_args()
    all_files = read_data(args.input_path)
    if not os.path.isdir(args.output_path):
        os.makedirs(args.output_path)
    for filename in all_files:
        detect_box(filename,args.output_path)





if __name__ == '__main__':
    main()