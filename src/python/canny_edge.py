from gaussian_blur import gaussian_blur
from intensity_gradient import intensity_gradient
import numpy as np
from PIL import Image
from skimage.color import rgb2hsv
import os

def main(): 
    # example image
    img = Image.open(os.path.join(os.path.dirname(__file__), '../../images/flower.jpg'))
    img.show()
    img = img.convert("L") # grayscale
    img_mat = np.array(img)

    # step 1: gaussian blur
    out = gaussian_blur(img_mat, iterations = 1)

    # step 2: finding intensity gradient
    out = intensity_gradient(out)
    
    img = Image.fromarray(out)
    img.show()

if __name__ == "__main__":
    main()