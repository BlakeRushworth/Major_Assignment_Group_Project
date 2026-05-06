"""
setup_check.py
--------------
Runs at application startup to:
    1. Verify the dataset folder exists and contains image classes
    2. Walk the user through selecting which species to analyse
    3. Return a validated config dict the rest of the app can use

If the dataset is missing, clear download instructions are printed and
the program exits gracefully rather than crashing later.
"""

import sys
from pathlib import Path

from src.config import RAW_DATA_DIR, SUPPORTED_EXTENSIONS


# Dataset validation 

def check_dataset_exists() -> bool:
    """Return True if RAW_DATA_DIR exists and contains at least one image.

    Returns bool
        True  – dataset is present and readable
        False – folder missing or completely empty
    """
    if not RAW_DATA_DIR.exists(): # checks if the directory exists
        return False

    # checks the filetype of the data within the directory
    for file in RAW_DATA_DIR.rglob("*"):
        if file.suffix.lower() in SUPPORTED_EXTENSIONS: # suffix.lower() makes the file extensions lowercase (jpeg, png, and etc) to avoid FileNotFoundError
            return True

    return False


def get_available_species() -> list[str]:
    """Scan RAW_DATA_DIR and return a sorted list of class folder names.

    Only immediate sub-folders that contain at least one supported image
    are returned.

    Returns list[str]
        Sorted class/species names found in the dataset.
    """
    species = [] # list to store all species
    for entry in sorted(RAW_DATA_DIR.iterdir()):
        if not entry.is_dir():
            continue
        # checks every file within the folder; if at least one image exists (.png, .jpeg, and etc), mark this folder as "has images"
        # any() stops as soon as it finds a match  
        has_images = any(f.suffix.lower() in SUPPORTED_EXTENSIONS for f in entry.iterdir()) # entry.iterdir() looks at everything within the current species folder 
        if has_images:
            species.append(entry.name)
    return species


def print_download_instructions() -> None:
    """Print friendly instructions for downloading the dataset."""
    print("\n" + "=" * 55)
    print("  Dataset not found")
    print("=" * 55)
    print(f"\nThe macroinvertebrate image dataset was not found at:{RAW_DATA_DIR}\n")
    print("To download the dataset:")
    print("1. Go to https://www.kaggle.com/datasets/kennethtm/stream-macroinvertebrates")
    print("2. Click 'Download' (you need a free Kaggle account)")
    print("3. Unzip the downloaded file")
    print(f"4. Move the extracted folders into:{RAW_DATA_DIR}")
    print("\nThe folder structure should look like:")
    print("    data/raw/")
    print("      Baetidae/")
    print("        image1.jpg")
    print("        image2.jpg")
    print("      Chironomidae/")
    print("        ...")
    print("\n  Then re-run the program.")
    print("=" * 55 + "\n")


# Species selection

def _print_species_list(available: list[str]) -> None:
    """Print the numbered species list used in the initial input screen."""
    print("=" * 55)
    print("\nInitial Input\n")
    print("=" * 55)
    for i, name in enumerate(available, 1): # enumarate(first-instance: iterable data, second-instance: start from)
        print(f"{i}. {name}")


def _parse_custom_input(raw: str, available: list[str]) -> list[str] | None:
    """Parse a comma-separated string of species names against the available list."""
    
    # builds a dictionary like {"baetidae": "Baetidae"} so we can match regardless of capitalisation
    lookup = {name.lower(): name for name in available}
    
    # splits the user's input by commas and strips whitespace from each piece e.g. "Baetidae, chironomidae" → ["Baetidae", "chironomidae"]
    parts = [p.strip() for p in raw.split(",") if p.strip()]

    if not parts:  # user just hit enter without typing anything
        print("\nNo species entered. Please try again.")
        return None

    selected = []      # species we successfully matched
    unrecognised = []  # species we couldn't find in the dataset

    for part in parts:
        if part.lower() in lookup:              # check against lowercase version of the name
            canonical = lookup[part.lower()]    # get the properly-cased name back e.g. "Baetidae"
            if canonical not in selected:       # avoid adding duplicates if user typed same one twice
                selected.append(canonical)
        else:
            unrecognised.append(part)  # couldn't find it, flag it for the error message

    if unrecognised:  # if anything didn't match, show the user what went wrong
        print(f"\nThese species were not recognised:")
        for name in unrecognised:
            print(f"X {name}")
        print("\nCheck the spelling against the list above and try again.")
        return None  # return None so the calling function knows to ask again

    return selected  # all names were valid, return the cleaned list


def prompt_species_selection(available: list[str]) -> list[str]:
    """Main species selection menu — keeps looping until user confirms a valid choice."""
    
    print("=" * 55)
    print("\nSetup Check\n")
    print("=" * 55)
    print("  PASSED  ")

    while True:  # keeps the menu running until we get a confirmed selection or exit
        _print_species_list(available)
        print("\n1.  Select all species")
        print("\n2.  Select a custom set")
        print("\n3.  Exit")
        choice = input("\n[Enter a number]: ").strip()

        if choice == "1":
            selected = available[:]  # [:] makes a copy of the list so we don't accidentally modify the original
            if _confirm_selection(selected):
                return selected      # confirmed — we're done, send the selection back
            # if they hit retry, the while True loop runs again and shows the menu again

        elif choice == "2":
            while True:  # inner loop just for the custom input — stays here until valid + confirmed or retried
                print("\n  Type the species you want, separated by commas.")
                print("  Example:  Baetidae, Chironomidae, Perlidae\n")
                raw = input("  Your selection: ").strip()

                selected = _parse_custom_input(raw, available)
                if selected is None:
                    continue  # _parse_custom_input already printed the error, just ask again

                if _confirm_selection(selected):
                    return selected  # confirmed — exit everything and return the list
                else:
                    break  # user hit retry — break out of inner loop, outer loop shows the main menu again

        elif choice == "3":
            print("\n  Exiting. Goodbye.\n")
            raise SystemExit(0)  # cleanly stops the whole program

        else:
            print("\n  Invalid choice. Please enter 1, 2, or 3.")


def _confirm_selection(selected: list[str]) -> bool:
    """Shows the user what they picked and asks them to confirm or go back."""
    
    print(f"\n  You selected {len(selected)} species:\n")
    for name in selected:
        print(f"      • {name}")

    print("\n  1.  Confirm and continue")
    print("  2.  Retry")
    
    while True:  # keeps asking until they enter 1 or 2
        answer = input("\n  [Enter a number]: ").strip()
        if answer == "1":
            return True   # confirmed
        if answer == "2":
            return False  # go back
        print("  Please enter 1 or 2.")


def run_setup() -> dict:
    """Runs at startup — checks the dataset exists, then handles species selection."""
    
    print("\n  Macroinvertebrate Image Analysis System")
    print("  Startup check…")

    if not check_dataset_exists():  # if no images found anywhere in data/raw/
        print_download_instructions()
        sys.exit(1)  # exit with code 1 meaning "something went wrong"

    available = get_available_species()  # get the list of class folder names

    if not available:  # folder exists but no valid sub-folders with images inside
        print(f"\nERROR: Dataset folder found at {RAW_DATA_DIR} but no class sub-folders with images were detected.\n"
               "Check that images are inside named sub-folders (one per species).\n")
        sys.exit(1)

    print(f"Dataset found ({len(available)} species available)")

    # prompt_species_selection handles the confirm/retry loop internally
    selected = prompt_species_selection(available)

    print("\n  Setup complete. Starting application…")
    print("=" * 55)

    return {
        "selected_species": selected,   # what the user chose
        "all_species": available,       # the full list, kept for reference
    }
