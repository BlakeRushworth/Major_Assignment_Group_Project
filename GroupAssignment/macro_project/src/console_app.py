import sys
from pathlib import Path
from PIL import Image
from tabulate import tabulate
from src.services.eda_service import EDAService
from src.config import AppConfig
from src.setup_check import run_setup
from src.services.image_manipulation_functions import Image_Manipulation_Functions
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

class ConsoleApp:
    """
    Console-based interface for the Macroinvertebrate Image Analysis System.

    Handles all user interaction after setup. Provides menus for viewing
    dataset summaries, generating charts, and applying image manipulations.

    Attributes
        workflow      : WorkflowService instance used to build and query the dataset.
        selection     : dict returned by run_setup() containing selected_species.
        df            : pd.DataFrame is built once at startup, shared across all menus.
        eda_service   : EDAService instance is initialised after the dataframe is ready.
    """
    def __init__(self, workflow, selection):
        self.workflow = workflow
        self.selection = selection
        self.df = None           # filled by run() before any menu is shown
        self.eda_service = None  # filled by run() after df is ready

    def run(self):
        """
        Entry point: indexes the dataset once, then launches the main menu.

        Building the dataframe here (rather than in __init__) means the heavy
        disk scan only happens once per session, and all menu options can reuse
        the same in-memory result.
        """
        print("\n[System] Preparing dataset...")
        self.df = self.workflow.initialize_data(self.selection["selected_species"])
        self.eda_service = EDAService(self.df,AppConfig.EDA_OUTPUT_DIR)
        self.main_menu()

    # Menus
    def main_menu(self):
        """
        Main navigation loop, it routes the user to sub-menus or exits.

        Keeps running until the user selects option 5 (close application).
        Invalid input is caught and re-prompted without crashing.
        """
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
                ConsoleApp.print_invalid_input(self)

    def dataset_summary_menu(self):
        """
        Display a statistical summary of the currently loaded dataset.

        Delegates to WorkflowService.display_summary(), which calls
        DatasetIndexer.get_summary() to print per-species stats.
        The input pause lets the user read before the menu redraws.
        """
        self.workflow.display_summary(self.df)
        user_check = input("\n[Press Enter to continue]: ")  # gives the user time to read before the menu goes back


    def graphs_menu(self):
        """
        Chart generation sub-menu, it lets the user choose which EDA chart to produce.

        Options 2–4 route to analysis_mode_menu() so the user can choose
        between an overall chart or a per-species breakdown.
        Option 1 (class distribution) always covers all species, so it goes
        straight to EDAService without a mode prompt.
        """
        while True:
            self.print_graph_menu()
            user_input = input("[Enter a number]: ")

            if user_input == "1":
                self.eda_service.save_class_distribution()
                print("\nSaved class distribution graph.")
                break

            elif user_input == "2":
                self.analysis_mode_menu("size")
                print("\nSaved image size distribution graph.")
                break

            elif user_input == "3":
                self.analysis_mode_menu("sample")
                print("\nSaved sample image grid.")
                break

            elif user_input == "4":
                self.analysis_mode_menu("brightness")
                print("\nSaved brightness distribution graph.")
                break

            elif user_input == "5":
                break

            else:
                self.print_invalid_input(self)

    def analysis_mode_menu(self, graph_type : str):
        """
        Secondary graph menu, to choose between overall or per-species output.

        Called by graphs_menu() after the chart type is already decided.
        The graph_type parameter determines which EDAService method is invoked.

        Parameters
            graph_type : str
                One of "size", "sample", or "brightness" which matches the three
                EDAService methods that support per_species mode.
        """
        while True:
            self.print_analysis_mode_menu()
            user_input = input("[Enter a number]: ")

            if user_input == "1":
                # Overall: one chart covering all selected species combined
                if graph_type == "size":
                    self.eda_service.save_image_size_distribution()
                elif graph_type == "sample":
                    self.eda_service.save_sample_grid()
                elif graph_type == "brightness":
                    self.eda_service.save_brightness_distribution()
                print("Saved overall graph.")

            elif user_input == "2":
                # Per species: one chart generated per species folder
                if graph_type == "size":
                    self.eda_service.save_image_size_distribution(per_species=True)
                elif graph_type == "sample":
                    self.eda_service.save_sample_grid(per_species=True)
                elif graph_type == "brightness":
                    self.eda_service.save_brightness_distribution(per_species=True)
                print("Saved per-species graphs.")

            elif user_input == "3":
                break # back to graphs_menu

            else:
                self.print_invalid_input(self)

    def image_manipulation_menu(self):
        """
        Image manipulation sub-menu, to apply transforms to a random sample per species.

        Each option picks one random image per species from the loaded dataframe,
        applies the chosen transformation, saves the result to
        data/processed/, and displays it via matplotlib.
        """
        while True:
            self.print_image_manipulation_menu()
            user_input = input("[Enter a number]: ")
            if user_input == "1":
                # Collect width and height before creating the manipulator
                resize_value: list = ConsoleApp.image_manipulation_resize_input(self)
                if resize_value is not None:
                    image_manipulation = Image_Manipulation_Functions()
                    image_manipulation.resize_img(self.df, resize_value)
            elif user_input == "2":
                image_manipulation = Image_Manipulation_Functions()
                image_manipulation.greyscale_img(self.df)
            elif user_input == "3":
                image_manipulation = Image_Manipulation_Functions()
                image_manipulation.invert_img(self.df)
            elif user_input == "4":
                print("going back")
                break
            else:
                self.print_invalid_input(self)

    def change_dataset(self):
        """
        Re-run the species selection flow and rebuild the dataframe.

        Lets the user switch to a different subset of species mid-session
        without restarting the program. The EDAService is also re-created
        so it references the fresh dataframe.
        """

        print("\n[System] Returning to dataset selection...\n")
        # run_setup() prompts the full species selection flow again
        self.selection = run_setup()
        # Rebuild the dataframe with the newly selected species
        self.df = self.workflow.initialize_data(
            self.selection["selected_species"]
        )
        # Re-create EDAService so it uses the updated dataframe
        self.eda_service = EDAService(
            self.df,
            AppConfig.EDA_OUTPUT_DIR
        )
        print("\n[System] Dataset updated successfully.\n")

    # Input validation
    def image_manipulation_resize_input(self):
        """Prompt the user for a target width and height for resizing."""
        try:
            resize_x_input: int = int(input("[Enter new image width size]: "))
        except ValueError:
            self.print_invalid_inputsize()
            return None
        try:
            resize_y_input: int = int(input("[Enter new image height size]: "))
        except ValueError:
            self.print_invalid_inputsize()
            return None
        return [int(resize_x_input), int(resize_y_input)]

    # Printing Menus
    def print_invalid_inputsize(self):
        """Print a specific error when a non-integer is entered for image dimensions."""
        print("=" * 55)
        print("\n ERROR: Input was not valid. Please enter a number (int). for example: 128 (units are in px) \n")
        print("=" * 55)
        user_check = input("[Press Enter to continue]: ")  # gives the user time to read before the menu goes back

    def print_close_application(self):
        """Print a goodbye message before the application exits."""
        print("=" * 55)
        print("\n  Closing Application \n")
        print("=" * 55)
        print("Closed.")

    def print_invalid_input(self):
        """Print a generic error when the user enters an option that does not exist."""
        print("=" * 55)
        print("\n ERROR: Input was not valid. Please press a number according to what you want selected. \n")
        print("=" * 55)
        user_check = input("[Press Enter to continue]: ")  # gives the user time to read before the menu goes back

    def print_invalid_filepath(self):
        """Print an error when a supplied file path does not exist or is not an image."""
        print("=" * 55)
        print("\n ERROR: file path given either wasn't found or wasn't an image. \n Please check file type and path of the image you are trying to select. \n")
        print("=" * 55)
        user_check = input("[Press Enter to continue]: ")  # gives the user time to read before the menu goes back

    def print_image_manipulation_menu(self):
        """Print the image manipulation sub-menu with three transform options."""
        rows = [
                ["  1: Resize image"],
                ["  2: Greyscale image"],
                ["  3: Invert image"],
                ["  4: Back \n"]
                ]
        print(tabulate(rows, headers=["Image Manipulation"], tablefmt="rounded_outline"))
    def print_graph_menu(self):
        """Print the chart generation sub-menu with four chart type options."""
        rows = [
                ["  1: Class Distribution"],
                ["  2: Image Size Distribution"],
                ["  3: Sample Image Grid"],
                ["  4: Brightness Distribution"],
                ["  5: Back"]
                ]
        print(tabulate(rows, headers=["Graphing Data Charts"], tablefmt="rounded_outline"))

    def print_analysis_mode_menu(self):
        """Print the analysis mode menu, the overall dataset vs per-species breakdown."""
        rows = [
                ["  1: Overall Selected Dataset"],
                ["  2: Per Species Chosen"],
                ["  3: Back"],
                ]
        print(tabulate(rows, headers=["Analysis Mode "], tablefmt="rounded_outline"))
    def print_main_menu(self):
        """Print the top-level application menu with all five navigation options."""
        rows = [
            ["  1: View Dataset Summary"],
            ["  2: Chart Generation"],
            ["  3: Image Manipulation"],
            ["  4: Choose Another Dataset"],
            ["  5: Close application \n"]
                ]
        print(tabulate(rows, headers=[ "Application"], tablefmt="rounded_outline"))
