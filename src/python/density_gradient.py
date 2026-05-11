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
    show_filter(grad, resize=False)

    # calculate the direction
    f = np.vectorize(calc_angle_lambda) 
    direction = f(grad_x, grad_y)

    # round the direction 
    round_direction_vec = np.vectorize(round_direction)
    rounded_direction = round_direction_vec(direction)
    
    return grad

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

