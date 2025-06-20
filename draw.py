'''
Wojciech Gorzynski
16-06-2025 v1

Program used for drawing a black and white image using a data matrix
'''

import numpy as np
import matplotlib.pyplot as plt
class Draw():
    def draw(data, px_size = 50, file_path= "qr_code.png"):
        height = len(data)
        width = len(data[0])
        image = np.zeros((height*px_size, width*px_size, 3), dtype=np.uint8)
        
        for i in range(height*px_size):
            for j in range(width*px_size):
                # black/white
                if data[i//px_size][j//px_size] == 0: # white
                    image[i,j] = [255,255,255]
                elif data[i//px_size][j//px_size] == 1: # black
                    image[i,j] = [0,0,0]
                # debugging    
                elif data[i//px_size][j//px_size] == -1: # blue
                    image[i,j] = [0,0,255]
                elif data[i//px_size][j//px_size] == -2: # green
                    image[i,j] = [0,255,0]
                elif data[i//px_size][j//px_size] == -3: # yellow
                    image[i,j] = [255,255,0]
                # blank  
                else:
                    image[i,j] = [255,0,0] # red
                    
        plt.imsave(file_path, image)