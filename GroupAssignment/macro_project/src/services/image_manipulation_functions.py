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
    def __init__(self):
        self.save_path_dir = Path(AppConfig.PROCESSED_DATA_DIR)
        self.save_path_dir.mkdir(parents=True, exist_ok=True)

    def resize_img(self, dataframe, new_size):
        count = 0
        for species in dataframe["species"].unique():
            count += 1
            species_df = dataframe[dataframe["species"] == species]
            random_row = species_df.sample(1).iloc[0]
            random_path = random_row["file_path"]

            img = load_img(random_path, target_size=(new_size[1], new_size[0])) #new size is a list with the first value height size and second width size
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
            print(f"\nImage successfully grayscaled Species({species}) into: {self.save_path_dir}")
    
    def invert_img(self, dataframe):
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
    
