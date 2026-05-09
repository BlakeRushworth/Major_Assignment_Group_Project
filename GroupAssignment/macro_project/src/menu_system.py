import sys
from PIL import Image
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.Functions.summary_functions import Summary_Functions
from src.Functions.graphs_functions import Graph_Functions
from src.Functions.image_manipulation_functions import Image_Manipulation_Functions

# menus --------------------------

def main_menu():
    summmary = Summary_Functions()
    graph = Graph_Functions()
    image_manipulation = Image_Manipulation_Functions()

    while True:
        print_main_menu()
        user_input = input("[Enter a number]: ")
        if user_input == "1":
            dataset_summary_menu()
        elif user_input == "2":
            graphs_menu()
        elif user_input == "3":
            image_manipulation_menu()
        elif user_input == "4":
            print_close_application()
            break
        else:
            print_invalid_input()

def dataset_summary_menu():
    while True:
        print_dataset_summary_menu()
        user_input = input("[Enter a number]: ")
        if user_input == "1":
            summmary = Summary_Functions()
            summmary.num_of_img()
            break
        elif user_input == "2":
            summmary = Summary_Functions()
            summmary.meta_data_average_each_species()
            break
        elif user_input == "3":
            summmary = Summary_Functions()
            summmary.meta_data_average_all_species()
            break
        elif user_input == "4":
            summmary = Summary_Functions()
            summmary.all()
            break
        elif user_input == "5":
            break
        else:
            print_invalid_input()

def graphs_menu():
    while True:
        print_graph_menu()
        user_input = input("[Enter a number]: ")
        if user_input == "1":
            graph = Graph_Functions()
            graph.option_1()
            break
        elif user_input == "2":
            graph = Graph_Functions()
            graph.option_2()
            break
        elif user_input == "3":
            graph = Graph_Functions()
            graph.option_3()
            break
        elif user_input == "4":
            break
        else:
            print_invalid_input()


def image_manipulation_menu():
    while True:
        print_image_manipulation_menu()
        user_input = input("[Enter a number]: ")
        if user_input == "1":
            filepath = image_manipulation_choose_image()
            if filepath is not None:
                image_manipulation = Image_Manipulation_Functions()
                image_manipulation.resize_img()
                break
        elif user_input == "2":
            filepath = image_manipulation_choose_image()
            if filepath is not None:
                image_manipulation = Image_Manipulation_Functions()
                image_manipulation.greyscale_img()
                break
        elif user_input == "3":
            filepath = image_manipulation_choose_image()
            if filepath is not None:
                image_manipulation = Image_Manipulation_Functions()
                image_manipulation.option_3()
                break
        elif user_input == "4":
            print("going back")
            break
        else:
            print_invalid_input()

# image manipulation checks -------------------------

def image_manipulation_choose_image():
    filepath_input = input("[Enter file path of Image]: ")
    if is_image(filepath_input):
        return filepath_input
    else:
        print_invalid_filepath()

def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verifies the file is actually an image
        return True
    except (IOError, SyntaxError):
        return False



#printing menu -------------------

def print_close_application():
    print("=" * 55)
    print("\n  Closing Application \n")
    print("=" * 55)
    print("Closed.")

def print_invalid_input():
    print("=" * 55)
    print("\n ERROR: Input was not valid. Please press a number according to what you want selected. \n")
    print("=" * 55)
    user_check = input("[Press Enter to continue]: ") # gives the user time to read before the menu goes back

def print_invalid_filepath():
    print("=" * 55)
    print("\n ERROR: file path given either wasnt found or wasnt an image. \n Please check file type and path of the image you are trying to select. \n")
    print("=" * 55)
    user_check = input("[Press Enter to continue]: ") # gives the user time to read before the menu goes back

def print_image_manipulation_menu():
    print("=" * 55)
    print("\n Image Manipulation \n")
    print("=" * 55)
    print("\n  1: Resize image")
    print("  2: Greyscale image")
    print("  3: option 3")
    print("  4: Back \n")

def print_dataset_summary_menu():
    print("=" * 55)
    print("\n Dataset Summary \n")
    print("=" * 55)
    print("\n  1: Number of Images")
    print("  2: Meta Data average for individual species")
    print("  3: Meta Data average for all species")
    print("  4: All of Above")
    print("  5: Back \n")

def print_graph_menu():
    print("=" * 55)
    print("\n Graphing Data \n")
    print("=" * 55)
    print("\n  1: option 1")
    print("  2: option 2")
    print("  3: option 3")
    print("  4: Back \n")

def print_main_menu():
    print("=" * 55)
    print("\n Application \n")
    print("=" * 55)
    print("\n  1: View Dataset Summary")
    print("  2: Generate Class Distribution Graph")
    print("  3: Image Manipulation")
    print("  4: Close application \n")

# -------------------------