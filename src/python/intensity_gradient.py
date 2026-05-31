import numpy as np
from PIL import Image
from math import degrees
from scipy import signal
from skimage.color import rgb2hsv, rgb2gray
import os
from convolve_util import convolve_rgb, convolve, show_filter

kernel_x = np.array([[1, 0], 
                    [0, -1]])

kernel_y = np.array([[0, 1], 
                     [-1, 0]])

def intensity_gradient(mono_img):
    grad_x = convolve(mat=mono_img, kernel=kernel_x)
    grad_y = convolve(mat=mono_img, kernel=kernel_y)

    f = np.vectorize(lambda x1, x2: np.arctan(x1, x2) - 3*np.pi/4) 
    direction = f(grad_x, grad_y)

    return direction
    

def intensity_gradient(mono_img):
    # get the matrix of values
    grad_x = convolve(mat=mono_img, kernel=kernel_x)
    grad_y = convolve(mat=mono_img, kernel=kernel_y)

    # calculate the magnitude gradient
    g = lambda x1, x2: np.sqrt(np.power(x1, 2) + np.power(x2, 2))
    grad = g(grad_x, grad_y)
    show_filter(grad, resize=False, save="images/intensity_gradient.png")

    # calculate the direction
    f = np.vectorize(calc_angle_lambda) 
    direction = f(grad_x, grad_y)

    # round the direction 
    round_direction_vec = np.vectorize(round_direction)
    rounded_direction = round_direction_vec(direction)

    # lower bound cutoff suppression
    grad = grad_magnitude_thresholding(grad, rounded_direction)
    show_filter(grad, resize=False, save="images/magnitude_th_intensity_gradient.png")
    
    return grad

def grad_magnitude_thresholding(gradient, direction): 
    out = np.zeros(gradient.shape)
    for x in range(1, gradient.shape[1]-1):
        for y in range(1, gradient.shape[0]-1):
            if(gradient[y,x] == 0.0): # skip non-edges
                continue

            if direction[y,x] == 0.0:
                region = gradient[y, x-1:x+2]
            if direction[y,x] == np.pi/4: 
                region = [gradient[y+1, x+1], gradient[y-1, x-1] ]
            if direction[y,x] == np.pi/2:
                region = gradient[y-1:y+2, x]
            if direction[y,x] == 3*np.pi/4:
                region = [ gradient[y+1, x-1], gradient[y-1, x+1] ]
            
            if (np.max(region) <= gradient[y,x]):
                out[y,x] = gradient[y,x]
    return out
            

def calc_angle_lambda(g_x, g_y):
    if (g_y == 0):
        return 0
    return np.arctan(g_x / g_y) - 3*np.pi/4

def round_direction(theta):
    rounded_dir = round(theta / (np.pi/4)) * (np.pi/4)

    # map to first 2 quadrants
    while (rounded_dir < 0):
        rounded_dir += np.pi

    if (abs(round_direction == np.pi)):
        rounded_dir = 0
    
    return rounded_dir

