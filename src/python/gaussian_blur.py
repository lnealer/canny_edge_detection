import numpy as np
from PIL import Image
from scipy import signal
import os

def gaussian_filter(size, sigma=2):
    kernel = np.fromfunction(lambda x, y: (1/(2*np.pi*sigma**2)) * np.exp(-((x-(size-1)/2)**2 + (y-(size-1)/2)**2)/(2*sigma**2)), (size, size))
    return kernel / np.sum(kernel) # normalize


def convolve(img, kernel):
    return signal.convolve2d(img, kernel,'same', boundary = 'fill', fillvalue = 0)


def gaussian_blur(img_mat, iterations = 1, kernel_size = 5, sigma = 2):
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

def show_filter():
    size = 5
    kernel = gaussian_filter(size, 1) * 255
    kernel_img =  np.array(Image.new(mode = "HSV", size=(size, size), color = (0,255,255)))
    kernel_img[:,:,2] = kernel
    img = Image.fromarray(kernel_img, mode = 'HSV').resize((300,300)).show()

def main(): 
    show_filter()
    # example
    img = Image.open(os.path.join(os.path.dirname(__file__), '../../images/flower.jpg'))
    img_mat = np.array(img)
    out = gaussian_blur(img_mat, iterations = 3)
    img = Image.fromarray(out)
    img.show()

if __name__ == "__main__":
    main()
