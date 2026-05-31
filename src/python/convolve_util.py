from scipy import signal
import numpy as np
from PIL import Image

def convolve(mat, kernel):
    return signal.convolve2d(mat, kernel,'same', boundary = 'fill', fillvalue = 0)

def convolve_rgb(mat, kernel):
        out_r = convolve(mat[:,:,0], kernel)
        out_g = convolve(mat[:,:,1], kernel)
        out_b = convolve(mat[:,:,2], kernel)
        return np.dstack((np.ceil(out_r).astype(np.uint8), 
                        np.ceil(out_g).astype(np.uint8), 
                        np.ceil(out_b).astype(np.uint8)))

def show_filter(kernel, resize=True, resize_x=300, resize_y=300, save=None):
    kernel = (kernel / np.max(kernel)) * 255 # normalize and rescale to 255
    size = (kernel.shape[1], kernel.shape[0])
    kernel_img =  np.array(Image.new(mode = "HSV", size=size, color = (255,0,255)))
    kernel_img[:,:,2] = kernel
    img = Image.fromarray(kernel_img, mode = 'HSV');
    if (resize):
         img = img.resize((resize_x, resize_y))  
    img.show()
    if save:
        img.convert('RGB').save(save, "PNG")