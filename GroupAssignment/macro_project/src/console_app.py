import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

class ConsoleApp:
    def __init__(self, workflow, selection):
        self.workflow = workflow
        self.selection = selection
        self.df = None  # We will fill this once

    def run(self):
        # Index the data once so it's ready for any menu option
        print("\n[System] Preparing dataset...")
        self.df = self.workflow.initialize_data(self.selection["selected_species"])
        self.main_menu()

    def main_menu(self):
        while True:
            self.print_main_menu()
            user_input = input("[Enter a number]: ")
            if user_input == "1":
                self.dataset_summary_menu()
            elif user_input == "2":
                self.graphs_menu()
            elif user_input == "3":
                self.image_manipulation_menu()
            elif user_input == "4":
                self.print_close_application()
                break
            else:
                ConsoleApp.print_invalid_input()

    def dataset_summary_menu(self):
        self.workflow.display_summary(self.df)

    def graphs_menu(self):
        while True:
            self.print_graph_menu()
            user_input = input("[Enter a number]: ")
            if user_input == "1":
                graph = self.Graph_Functions()
                graph.option_1()
                break
            elif user_input == "2":
                graph = self.Graph_Functions()
                graph.option_2()
                break
            elif user_input == "3":
                graph = self.Graph_Functions()
                graph.option_3()
                break
            elif user_input == "4":
                break
            else:
                self.print_invalid_input()

    def image_manipulation_menu(self):
        while True:
            self.print_image_manipulation_menu()
            user_input = input("[Enter a number]: ")
            if user_input == "1":
                filepath = self.image_manipulation_choose_image()
                if filepath is not None:
                    image_manipulation = self.Image_Manipulation_Functions()
                    image_manipulation.resize_img()
                    break
            elif user_input == "2":
                filepath = ConsoleApp.image_manipulation_choose_image()
                if filepath is not None:
                    image_manipulation = self.Image_Manipulation_Functions()
                    image_manipulation.greyscale_img()
                    break
            elif user_input == "3":
                filepath = ConsoleApp.image_manipulation_choose_image()
                if filepath is not None:
                    image_manipulation = self.Image_Manipulation_Functions()
                    image_manipulation.option_3()
                    break
            elif user_input == "4":
                print("going back")
                break
            else:
                self.print_invalid_input()

    # image manipulation checks -------------------------

    def image_manipulation_choose_image(self):
        filepath_input = input("[Enter file path of Image]: ")
        if is_image(filepath_input):
            return filepath_input
        else:
            self.print_invalid_filepath()

    def is_image(self, file_path):
        try:
            with Image.open(file_path) as img:
                img.verify()  # Verifies the file is actually an image
            return True
        except (IOError, SyntaxError):
            return False

    # printing menu -------------------

    def print_close_application(self):
        print("=" * 55)
        print("\n  Closing Application \n")
        print("=" * 55)
        print("Closed.")

    def print_invalid_input(self):
        print("=" * 55)
        print("\n ERROR: Input was not valid. Please press a number according to what you want selected. \n")
        print("=" * 55)
        user_check = input("[Press Enter to continue]: ")  # gives the user time to read before the menu goes back

    def print_invalid_filepath(self):
        print("=" * 55)
        print(
            "\n ERROR: file path given either wasnt found or wasnt an image. \n Please check file type and path of the image you are trying to select. \n")
        print("=" * 55)
        user_check = input("[Press Enter to continue]: ")  # gives the user time to read before the menu goes back

    def print_image_manipulation_menu(self):
        print("=" * 55)
        print("\n Image Manipulation \n")
        print("=" * 55)
        print("\n  1: Resize image")
        print("  2: Greyscale image")
        print("  3: option 3")
        print("  4: Back \n")

    def print_graph_menu(self):
        print("=" * 55)
        print("\n Graphing Data \n")
        print("=" * 55)
        print("\n  1: option 1")
        print("  2: option 2")
        print("  3: option 3")
        print("  4: Back \n")

    def print_main_menu(self):
        print("=" * 55)
        print("\n Application \n")
        print("=" * 55)
        print("\n  1: View Dataset Summary")
        print("  2: Generate Class Distribution Graph")
        print("  3: Image Manipulation")
        print("  4: Close application \n")