#I used some code from the week 5 work for assignment 2 to select and show the images that the programs creates and saves.
#I altered that code to get a random filename instead, a loop system for all the species and the altering of the images themselves.


import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
from src.config import AppConfig
from pathlib import Path
Path(AppConfig.PROCESSED_DATA_DIR).mkdir(parents=True, exist_ok=True)
from keras.preprocessing.image import load_img
from keras.preprocessing.image import save_img
from keras.preprocessing.image import img_to_array


class Image_Manipulation_Functions:
    """
    Apply image transformations to a random sample from each selected species.

    For every method, one image per species is randomly selected from the
    provided DataFrame, the transformation is applied, the result is saved
    to data/processed/, and then displayed in a matplotlib window.

    Attributes
        save_path_dir : Path to the processed output folder, created on init
    """
    def __init__(self):
        self.save_path_dir = Path(AppConfig.PROCESSED_DATA_DIR)
        self.save_path_dir.mkdir(parents=True, exist_ok=True)

    def resize_img(self, dataframe, new_size):
        """
        Resize one random image per species and save + display the result.

        Uses Keras load_img() with target_size so the resize is handled
        cleanly without manual cv2 interpolation calls.

        Parameters
            dataframe : pd.DataFrame
                The indexed dataset, must contain 'species' and 'file_path' columns.
            new_size  : list[int]
                [width, height] in pixels, note load_img takes (height, width)
                so the values are swapped when passed in.
        """
        count = 0
        for species in dataframe["species"].unique():
            count += 1
            species_df = dataframe[dataframe["species"] == species]
            random_row = species_df.sample(1).iloc[0]
            random_path = random_row["file_path"]

            img = load_img(random_path, target_size=(new_size[1], new_size[0])) # new size is a list with the first value height size and second width size
            # convert image to a numpy array
            img_array = img_to_array(img)
            save_filename = 'species_re-sized('+str(count)+').jpg'
            #print(f"{save_filename = }")
            full_save_path = os.path.join(self.save_path_dir, save_filename)
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
            print(f"\nImage successfully re-sized into: {self.save_path_dir}")

    def greyscale_img(self, dataframe):
        """
        Convert one random image per species to greyscale and save + display it.

        Passing color_mode='grayscale' to load_img handles the colour
        channel conversion internally, producing a single-channel image.

        Parameters
            dataframe : pd.DataFrame
                The indexed dataset, must contain 'species' and 'file_path' columns.
        """
        count = 0
        for species in dataframe["species"].unique():
            count += 1
            species_df = dataframe[dataframe["species"] == species]
            random_row = species_df.sample(1).iloc[0]
            random_path = random_row["file_path"]

            img = load_img(random_path, color_mode='grayscale')
            # convert image to a numpy array
            img_array = img_to_array(img)
            save_filename = 'species_grayscaled('+str(count)+').jpg'
            full_save_path = os.path.join(self.save_path_dir, save_filename)
            save_img(full_save_path, img_array)
            # load the image to confirm it was saved correctly
            img = load_img(full_save_path)
            plt.imshow(img)
            plt.axis('off') # Turn off axis labels
            plt.show()
            print(f"\nImage successfully grayscaled Species({species}) into: {self.save_path_dir}")
    
    def invert_img(self, dataframe):
        """
        Invert the pixel values of one random image per species and save + display it.

        Inversion is performed by subtracting each pixel value from 255
        (the maximum 8-bit value). This flips light pixels dark and vice versa.

        Parameters
            dataframe : pd.DataFrame
                The indexed dataset, must contain 'species' and 'file_path' columns.
        """
        count = 0
        for species in dataframe["species"].unique():
            count += 1
            species_df = dataframe[dataframe["species"] == species]
            random_row = species_df.sample(1).iloc[0]
            random_path = random_row["file_path"]

            img = load_img(random_path, color_mode='rgb')
            # convert image to a numpy array
            img_array = img_to_array(img)
            save_filename = 'species_inverted('+str(count)+').jpg'
            #print(f"{save_filename = }")
            full_save_path = os.path.join(self.save_path_dir, save_filename)

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
            print(f"\nImage successfully inverted Species({species}) into: {self.save_path_dir}")
    
