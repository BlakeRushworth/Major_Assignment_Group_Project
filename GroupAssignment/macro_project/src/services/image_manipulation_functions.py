import matplotlib.pyplot as plt
import os

import cv2
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import save_img
from keras.preprocessing.image import img_to_array


class Image_Manipulation_Functions:
    def resize_img(self, filepath, new_size):
        img = load_img(filepath, target_size=(new_size[1], new_size[0])) #new size is a list with the first value height size and second width size
        # convert image to a numpy array
        img_array = img_to_array(img)
        # save the image with a new filename
        save_path_dir = 'data\processed'
        save_filename = 'species_re-sized.jpg'
        #print(f"{save_filename = }")
        full_save_path = os.path.join(save_path_dir, save_filename)
        save_img(full_save_path, img_array)
        # load the image to confirm it was saved correctly
        img = load_img(full_save_path)
        # print(type(img))
        # print(img.format)
        # print(img.mode)
        # print(img.size)
        # # show the image using matplotlib
        plt.imshow(img)
        plt.axis('off') # Turn off axis labels
        plt.show()
        print(f"\nimage successfully re-sized into: {save_path_dir}")

    def greyscale_img(self, filepath):
        img = load_img(filepath, color_mode='grayscale')
        # convert image to a numpy array
        img_array = img_to_array(img)
        # save the image with a new filename
        save_path_dir = 'data\processed'
        save_filename = 'species_grayscaled.jpg'
        #print(f"{save_filename = }")
        full_save_path = os.path.join(save_path_dir, save_filename)
        save_img(full_save_path, img_array)
        # load the image to confirm it was saved correctly
        img = load_img(full_save_path)
        # print(type(img))
        # print(img.format)
        # print(img.mode)
        # print(img.size)
        # # show the image using matplotlib
        plt.imshow(img)
        plt.axis('off') # Turn off axis labels
        plt.show()
        print(f"\nimage successfully grayscaled into: {save_path_dir}")
    
    def invert_img(self, filepath):
        img = load_img(filepath, color_mode='rgb')
        # convert image to a numpy array
        img_array = img_to_array(img)
        # save the image with a new filename
        save_path_dir = 'data\processed'
        save_filename = 'species_inverted.jpg'
        #print(f"{save_filename = }")
        full_save_path = os.path.join(save_path_dir, save_filename)

        inverted_img_array = 255 - img_array
        save_img(full_save_path, inverted_img_array)
        # load the image to confirm it was saved correctly
        img = load_img(full_save_path)
        # print(type(img))
        # print(img.format)
        # print(img.mode)
        # print(img.size)
        # # show the image using matplotlib
        plt.imshow(img)
        plt.axis('off') # Turn off axis labels
        plt.show()
        print(f"\nimage successfully inverted into: {save_path_dir}")
    