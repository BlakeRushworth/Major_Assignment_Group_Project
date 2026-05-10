import sys
from pathlib import Path
from src.services.eda_service import EDAService
from src.config import AppConfig
from src.setup_check import run_setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

class ConsoleApp:
    def __init__(self, workflow, selection):
        self.workflow = workflow
        self.selection = selection
        self.df = None  # We will fill this once
        self.eda_service = None

    def run(self):
        # Index the data once so it's ready for any menu option
        print("\n[System] Preparing dataset...")
        self.df = self.workflow.initialize_data(self.selection["selected_species"])
        self.eda_service = EDAService(self.df,AppConfig.EDA_OUTPUT_DIR)
        self.main_menu()

    def post_action_navigation(self):
        print("\n" + "-" * 20)
        print("1. Back to Menu")
        print("2. Exit Program")

        choice = input("\n[Select an option]: ")

        if choice == "2":
            self.print_close_application()
            sys.exit()

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
                self.change_dataset()
            elif user_input == "5":
                self.print_close_application()
                break
            
            else:
                ConsoleApp.print_invalid_input()

    def dataset_summary_menu(self):
        self.workflow.display_summary(self.df)
        self.post_action_navigation()

    def graphs_menu(self):

        while True:

            self.print_graph_menu()

            user_input = input("[Enter a number]: ")

            if user_input == "1":
                self.eda_service.save_class_distribution()
                print("Saved class distribution graph.")

            elif user_input == "2":
                self.analysis_mode_menu("size")
                print("Saved image size distribution graph.")

            elif user_input == "3":
                self.analysis_mode_menu("sample")
                print("Saved sample image grid.")

            elif user_input == "4":
                self.analysis_mode_menu("brightness")
                print("Saved brightness distribution graph.")

            elif user_input == "5":
                break

            else:
                self.print_invalid_input()

    def analysis_mode_menu(self, graph_type : str):

        while True:

            self.print_analysis_mode_menu()

            user_input = input("[Enter a number]: ")

            if user_input == "1":

                if graph_type == "size":
                    self.eda_service.save_image_size_distribution()

                elif graph_type == "sample":
                    self.eda_service.save_sample_grid()

                elif graph_type == "brightness":
                    self.eda_service.save_brightness_distribution()

                print("Saved overall graph.")

            elif user_input == "2":

                if graph_type == "size":
                    self.eda_service.save_image_size_distribution(per_species=True)

                elif graph_type == "sample":
                    self.eda_service.save_sample_grid(per_species=True)

                elif graph_type == "brightness":
                    self.eda_service.save_brightness_distribution(per_species=True)

                print("Saved per-species graphs.")

            elif user_input == "3":
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
        print("\n Graphing Data Charts\n")
        print("=" * 55)
        print("\n  1: Class Distribution")
        print("  2: Image Size Distribution")
        print("  3: Sample Image Grid")
        print("  4: Brightness Distribution")
        print("  5: Back \n")

    def print_analysis_mode_menu(self):

        print("=" * 55)
        print("\n Analysis Mode \n")
        print("=" * 55)

        print("\n  1: Overall Selected Dataset")
        print("  2: Per Species Chosen")
        print("  3: Back\n")

    def print_main_menu(self):
        print("=" * 55)
        print("\n Application \n")
        print("=" * 55)
        print("\n  1: View Dataset Summary")
        print("  2: Chart Generation")
        print("  3: Image Manipulation")
        print("  4: Choose Another Dataset \n")
        print("  5: Close application \n")

    def change_dataset(self):

        print("\n[System] Returning to dataset selection...\n")

        self.selection = run_setup()

        self.df = self.workflow.initialize_data(
            self.selection["selected_species"]
        )

        self.eda_service = EDAService(
            self.df,
            AppConfig.EDA_OUTPUT_DIR
        )

        print("\n[System] Dataset updated successfully.\n")