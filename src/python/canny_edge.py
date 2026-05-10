from gaussian_blur import gaussian_blur
import numpy as np
from PIL import Image
import os

def main(): 
    # example image
    img = Image.open(os.path.join(os.path.dirname(__file__), '../../images/flower.jpg'))
    img_mat = np.array(img)

    # step 1: gaussian blur
    out = gaussian_blur(img_mat, iterations = 1)
    
    img = Image.fromarray(out)
    img.show()

if __name__ == "__main__":
    main()