import numpy as np
from PIL import Image
from convolve_util import convolve, show_filter
from skimage.color import rgb2gray
import os

def gaussian_filter(size, sigma=2):
    kernel = np.fromfunction(lambda x, y: (1/(2*np.pi*sigma**2)) * np.exp(-((x-(size-1)/2)**2 + (y-(size-1)/2)**2)/(2*sigma**2)), (size, size))
    return kernel / np.sum(kernel) # normalize

def gaussian_blur_rgb(img_mat, iterations = 1, kernel_size = 5, sigma = 2):
    i = 0
    reformed_img = img_mat
    kernel = gaussian_filter(kernel_size, sigma)
    while (i < iterations):
        out_r = convolve(img_mat[:,:,0], kernel)
        out_g = convolve(img_mat[:,:,1], kernel)
        out_b = convolve(img_mat[:,:,2], kernel)
        reformed_img = np.dstack((np.ceil(out_r).astype(np.uint8), 
                        np.ceil(out_g).astype(np.uint8), 
                        np.ceil(out_b).astype(np.uint8)))
        img_mat = reformed_img
        i += 1
    return reformed_img 


def gaussian_blur(img_mat, iterations = 1, kernel_size = 5, sigma = 2):
    i = 0
    out = img_mat
    kernel = gaussian_filter(kernel_size, sigma)
    while (i < iterations):
        out = convolve(out, kernel)
        i += 1
    return out 



def main(): 
    show_filter(gaussian_filter(5, 1))
    # example
    img = Image.open(os.path.join(os.path.dirname(__file__), '../../images/flower.jpg'))
    mono_img = img.convert("L")
    img_mat = np.array(mono_img)
    out = gaussian_blur(img_mat, iterations = 3)
    img = Image.fromarray(out)
    img.show()

if __name__ == "__main__":
    main()
