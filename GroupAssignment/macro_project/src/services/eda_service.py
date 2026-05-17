from pathlib import Path
import os
import matplotlib.pyplot as plt
import cv2
import pandas as pd
import seaborn as sns
class EDAService:
    """
    Generate and save Exploratory Data Analysis (EDA) outputs for the indexed image dataset.

    Every public method follows the same pattern:
        1. Create a dedicated output subfolder inside output_dir.
        2. Clear any old PNG files from that folder so stale results don't accumulate.
        3. Generate the chart(s) with matplotlib/seaborn.
        4. Save the PNG(s) to disk and open the folder in File Explorer.

    Most methods accept a per_species flag; when True, one chart is produced
    per species folder; when False (default), a single chart covers the whole dataset.

    Attributes
        dataframe  : pd.DataFrame is the indexed image dataset built by DatasetIndexer.
        output_dir : Path — root folder where all EDA subfolders are created.
    """
    
    def __init__(
        self,
        dataframe: pd.DataFrame,
        output_dir: Path
    ) -> None:

        self.dataframe = dataframe
        self.output_dir = output_dir
        # Create the root output folder immediately so later mkdir calls never fail
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_class_distribution(self) -> None:
        """
        Save a bar chart showing the number of images per species class.

        Always covers the full selected dataset, so no per_species mode needed
        because the chart itself already separates species on the x-axis.
        The species are ordered [from most to least] images for readability.
        """
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "class_distribution_charts"
        base_dir.mkdir(parents=True, exist_ok=True)
        self._clear_png_files(base_dir) # remove previous version before saving a fresh one

        plt.figure(figsize=(12, 6))
        # value_counts().index gives species names sorted by frequency, highest first
        order = self.dataframe["species"].value_counts().index
        sns.countplot(data=self.dataframe, x="species", order=order)

        plt.xticks(rotation=90) # rotate labels so long species names don't overlap
        plt.title("Macroinvertebrate Images per Class")
        plt.tight_layout()
        plt.savefig(base_dir / "class_distribution.png")
        self._open_directory(base_dir)
        plt.close()
    
    def save_image_size_distribution(self,per_species: bool = False) -> None:
        """
        Save side-by-side histograms of image pixel width and height.

        Parameters
            per_species : bool
                False (default): one chart covering all selected species.
                True: one chart per species, saved into a per_species subfolder.
        """
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "image_size_charts"
        base_dir.mkdir(parents=True, exist_ok=True)
        self._clear_png_files(base_dir)
        if per_species:

            species_dir = base_dir / "per_species"

            species_dir.mkdir(
                parents=True,
                exist_ok=True
            )
            self._clear_png_files(species_dir)
            for species in self.dataframe["species"].unique():
                # Filter the dataframe down to just this species' rows
                species_df = self.dataframe[
                    self.dataframe["species"] == species
                ]

                fig, axes = plt.subplots(
                    1,
                    2,
                    figsize=(12, 5)
                )

                sns.histplot(
                    species_df["width"],
                    bins=20,
                    ax=axes[0]
                )

                sns.histplot(
                    species_df["height"],
                    bins=20,
                    ax=axes[1]
                )

                axes[0].set_title(
                    f"{species} Width Distribution"
                )

                axes[1].set_title(
                    f"{species} Height Distribution"
                )

                plt.tight_layout()

                plt.savefig(
                    species_dir /
                    f"{species}_image_size_distribution.png"
                )
                self._open_directory(species_dir)
                plt.close()

        else:

            fig, axes = plt.subplots(
                1,
                2,
                figsize=(12, 5)
            )

            sns.histplot(
                self.dataframe["width"],
                bins=20,
                ax=axes[0]
            )

            sns.histplot(
                self.dataframe["height"],
                bins=20,
                ax=axes[1]
            )

            axes[0].set_title(
                "Image Width Distribution"
            )

            axes[1].set_title(
                "Image Height Distribution"
            )

            plt.tight_layout()

            plt.savefig(
                base_dir /
                "image_size_distribution.png"
            )
            self._open_directory(base_dir)
            plt.close()

    def save_sample_grid(self,per_species: bool = False,sample_count: int = 9) -> None:
        """
        Save a 3×3 grid of randomly sampled images from the dataset.

        Images are loaded with OpenCV and converted from BGR to RGB before
        display, then OpenCV reads in BGR order but matplotlib expects RGB.

        Parameters
            per_species  : bool
                False (default): one grid sampled across all species.
                True: one grid per species from that species' images only.
            sample_count : int
                Maximum number of images to include in the grid (default 9).
                min() ensures we never request more samples than exist.
        """
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "sample_grids"
        base_dir.mkdir(parents=True, exist_ok=True)
        self._clear_png_files(base_dir)
        if per_species:

            species_dir = base_dir / "per_species"

            species_dir.mkdir(
                parents=True,
                exist_ok=True
            )
            self._clear_png_files(species_dir)
            for species in self.dataframe["species"].unique():

                species_df = self.dataframe[
                    self.dataframe["species"] == species
                ]
                # random_state=42 makes the sample reproducible across runs
                sample_df = species_df.sample(
                    min(sample_count, len(species_df)),
                    random_state=42
                )

                fig, axes = plt.subplots(
                    3,
                    3,
                    figsize=(10, 10)
                )

                for ax, (_, row) in zip(
                    axes.flat,
                    sample_df.iterrows()
                ):

                    image = cv2.imread(
                        row["file_path"]
                    )

                    image = cv2.cvtColor(
                        image,
                        cv2.COLOR_BGR2RGB
                    )  # convert BGR → RGB for matplotlib

                    ax.imshow(image)

                    ax.set_title(
                        row["species"]
                    )

                    ax.axis("off")
                # Hide any empty grid cells if sample_df has fewer than 9 rows
                for ax in axes.flat[len(sample_df):]:
                    ax.axis("off")

                plt.tight_layout()

                plt.savefig(
                    species_dir /
                    f"{species}_sample_grid.png"
                )
                self._open_directory(species_dir)
                plt.close()

        else:

            sample_df = self.dataframe.sample(
                min(sample_count, len(self.dataframe)),
                random_state=42
            )

            fig, axes = plt.subplots(
                3,
                3,
                figsize=(10, 10)
            )

            for ax, (_, row) in zip(
                axes.flat,
                sample_df.iterrows()
            ):

                image = cv2.imread(
                    row["file_path"]
                )

                image = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2RGB
                )

                ax.imshow(image)

                ax.set_title(
                    row["species"]
                )

                ax.axis("off")

            for ax in axes.flat[len(sample_df):]:
                ax.axis("off")

            plt.tight_layout()

            plt.savefig(
                base_dir /
                "sample_grid.png"
            )
            self._open_directory(base_dir)
            plt.close()

    def save_brightness_distribution(self,per_species: bool = False) -> None:
        """
        Save a histogram of mean greyscale brightness values across images.

        Brightness is calculated by loading each image in greyscale mode and
        taking the mean pixel value (0 = black, 255 = white).

        Parameters
            per_species : bool
                False (default): one histogram across all selected species.
                True: one histogram per species.
        """
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "brightness_charts"
        base_dir.mkdir(parents=True, exist_ok=True)
        self._clear_png_files(base_dir)
        if per_species:
            
            species_dir = base_dir / "per_species"

            species_dir.mkdir(
                parents=True,
                exist_ok=True
            )
            self._clear_png_files(species_dir)
            for species in self.dataframe["species"].unique():

                species_df = self.dataframe[
                    self.dataframe["species"] == species
                ]

                brightness_values = []

                for path in species_df["file_path"]:

                    image = cv2.imread(
                        path,
                        cv2.IMREAD_GRAYSCALE
                    )

                    if image is not None: # skip any unreadable files silently
                        brightness_values.append(
                            image.mean()
                        )

                plt.figure(figsize=(10, 5))

                sns.histplot(
                    brightness_values,
                    bins=20
                )

                plt.title(
                    f"{species} Brightness Distribution"
                )

                plt.xlabel(
                    "Average Brightness"
                )

                plt.ylabel("Count")

                plt.tight_layout()

                plt.savefig(
                    species_dir /
                    f"{species}_brightness_distribution.png"
                )
                self._open_directory(species_dir)
                plt.close()

        else:

            brightness_values = []

            for path in self.dataframe["file_path"]:

                image = cv2.imread(
                    path,
                    cv2.IMREAD_GRAYSCALE
                )

                if image is not None:
                    brightness_values.append(
                        image.mean()
                    )

            plt.figure(figsize=(10, 5))

            sns.histplot(
                brightness_values,
                bins=20
            )

            plt.title(
                "Image Brightness Distribution"
            )

            plt.xlabel(
                "Average Brightness"
            )

            plt.ylabel("Count")

            plt.tight_layout()

            plt.savefig(
                base_dir /
                "brightness_distribution.png"
            )
            self._open_directory(base_dir)
            plt.close()

    def save_width_height_scatter_plot(self,per_species: bool = False) -> None:
        """
        ave a scatter plot of image width vs height.

        Useful for spotting whether all images share the same aspect ratio
        or if there are outliers with unusual dimensions.
        The overall (non per-species) version colours each point by species
        using the hue parameter so clusters are visible in one chart.

        Parameters
            per_species : bool
                False (default): one scatter plot with all species colour-coded.
                True: one scatter plot per species.
        """
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "scatter_plots"

        base_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self._clear_png_files(base_dir)

        if per_species:

            species_dir = base_dir / "per_species"

            species_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            self._clear_png_files(species_dir)

            for species in self.dataframe["species"].unique():

                species_df = self.dataframe[
                    self.dataframe["species"] == species
                ]

                plt.figure(figsize=(8, 6))

                sns.scatterplot(
                    data=species_df,
                    x="width",
                    y="height"
                )

                plt.title(
                    f"{species} Width vs Height"
                )

                plt.xlabel("Width")
                plt.ylabel("Height")

                plt.tight_layout()

                plt.savefig(
                    species_dir /
                    f"{species}_scatter_plot.png"
                )

                plt.close()

            self._open_directory(species_dir)

        else:

            plt.figure(figsize=(8, 6))
            # hue="species" colour-codes each point so all species are visible in one chart
            sns.scatterplot(
                data=self.dataframe,
                x="width",
                y="height",
                hue="species"
            )

            plt.title(
                "Image Width vs Height"
            )

            plt.xlabel("Width")
            plt.ylabel("Height")

            plt.tight_layout()

            plt.savefig(
                base_dir /
                "scatter_plot.png"
            )

            plt.close()

            self._open_directory(base_dir)

    def save_width_boxplot(self,per_species: bool = False) -> None:
        """
        Save a boxplot of image widths to highlight spread and outliers.

        Boxplots show the median, interquartile range, and outliers, making
        it easy to see if any species has unusually wide or narrow images.

        Parameters
            per_species : bool
                False (default): one grouped boxplot with all species on the x-axis.
                True: one boxplot per species.
        """
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "width_boxplots"

        base_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self._clear_png_files(base_dir)

        if per_species:

            species_dir = base_dir / "per_species"

            species_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            self._clear_png_files(species_dir)

            for species in self.dataframe["species"].unique():

                species_df = self.dataframe[
                    self.dataframe["species"] == species
                ]

                plt.figure(figsize=(6, 5))

                sns.boxplot(
                    y=species_df["width"]
                )

                plt.title(
                    f"{species} Width Boxplot"
                )

                plt.ylabel("Width")

                plt.tight_layout()

                plt.savefig(
                    species_dir /
                    f"{species}_width_boxplot.png"
                )

                plt.close()

            self._open_directory(species_dir)

        else:

            plt.figure(figsize=(10, 6))

            sns.boxplot(
                data=self.dataframe,
                x="species",
                y="width"
            )

            plt.xticks(rotation=45)  # rotate so long species names don't overlap

            plt.title(
                "Width by Species"
            )

            plt.tight_layout()

            plt.savefig(
                base_dir /
                "width_boxplot.png"
            )

            plt.close()

            self._open_directory(base_dir)


    def save_height_boxplot(self,per_species: bool = False) -> None:
        """
        Save a boxplot of image heights to highlight spread and outliers.

        Mirror of save_width_boxplot, same structure but for the height column.

        Parameters
            per_species : bool
                False (default): one grouped boxplot with all species on the x-axis.
                True: one boxplot per species.
        """
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "height_boxplots"

        base_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self._clear_png_files(base_dir)

        if per_species:

            species_dir = base_dir / "per_species"

            species_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            self._clear_png_files(species_dir)

            for species in self.dataframe["species"].unique():

                species_df = self.dataframe[
                    self.dataframe["species"] == species
                ]

                plt.figure(figsize=(6, 5))

                sns.boxplot(
                    y=species_df["height"]
                )

                plt.title(
                    f"{species} Height Boxplot"
                )

                plt.ylabel("Height")

                plt.tight_layout()

                plt.savefig(
                    species_dir /
                    f"{species}_height_boxplot.png"
                )

                plt.close()

            self._open_directory(species_dir)

        else:

            plt.figure(figsize=(10, 6))

            sns.boxplot(
                data=self.dataframe,
                x="species",
                y="height"
            )

            plt.xticks(rotation=45) # rotate so long species names don't overlap

            plt.title(
                "Height by Species"
            )

            plt.tight_layout()

            plt.savefig(
                base_dir /
                "height_boxplot.png"
            )

            plt.close()

            self._open_directory(base_dir)

    def save_pixel_intensity_histogram(self,per_species: bool = False) -> None:
        """
        Save a histogram of raw greyscale pixel intensity values (0–255).

        Unlike save_brightness_distribution() which uses one mean value per image,
        this method flattens the entire pixel array for each image so every
        individual pixel contributes to the histogram, giving it a more detailed
        view of the tonal range across the dataset.

        Parameters
            per_species : bool
                False (default): one histogram across all selected species.
                True: one histogram per species.
        """
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "pixel_histograms"

        base_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self._clear_png_files(base_dir)

        if per_species:

            species_dir = base_dir / "per_species"

            species_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            self._clear_png_files(species_dir)
            for species in self.dataframe["species"].unique():

                species_df = self.dataframe[
                    self.dataframe["species"] == species
                ]

                intensity_values = []

                for path in species_df["file_path"]:

                    grayscale = cv2.imread(
                        path,
                        cv2.IMREAD_GRAYSCALE
                    )

                    if grayscale is not None:
                        # flatten() converts the 2D pixel grid into a 1D list of values
                        intensity_values.extend(
                            grayscale.flatten()
                        )

                plt.figure(figsize=(9, 6))

                sns.histplot(
                    intensity_values,
                    bins=50
                )

                plt.title(
                    f"{species} Pixel Intensity Histogram"
                )

                plt.xlabel(
                    "Pixel Intensity"
                )

                plt.ylabel("Frequency")

                plt.tight_layout()

                plt.savefig(
                    species_dir /
                    f"{species}_pixel_histogram.png"
                )

                plt.close()

            self._open_directory(species_dir)

        else:

            intensity_values = []
            for path in self.dataframe["file_path"]:

                grayscale = cv2.imread(
                    path,
                    cv2.IMREAD_GRAYSCALE
                )

                if grayscale is not None:

                    intensity_values.extend(
                        grayscale.flatten()
                    )

            plt.figure(figsize=(9, 6))

            sns.histplot(
                intensity_values,
                bins=50
            )

            plt.title(
                "Pixel Intensity Histogram"
            )

            plt.xlabel(
                "Pixel Intensity"
            )

            plt.ylabel("Frequency")

            plt.tight_layout()

            plt.savefig(
                base_dir /
                "pixel_histogram.png"
            )

            plt.close()

            self._open_directory(base_dir)

    def build_summary(self) -> dict[str, float]:
        """
        Return key dataset statistics as a dictionary.

        Used by both the console summary menu and the GUI dashboard to display
        top-level numbers without re-querying the DataFrame in multiple places.
        """

        return {
        "total_images": int(len(self.dataframe)),
        "total_classes": int(self.dataframe["species"].nunique()),
        "mean_width": float(self.dataframe["width"].mean()),
        "mean_height": float(self.dataframe["height"].mean()),
        }
    
    def _clear_png_files(self, directory: Path) -> None:
        """
        Delete all PNG files in a directory before saving fresh output.

        Prevents old charts from accumulating if the user runs the same
        analysis multiple times. PermissionError is caught and reported
        rather than crashing, this can happen if a file is open in an image viewer.

        Parameters
            directory : Path of the folder to clean.
        """

        for file in directory.glob("*.png"):

            try:
                file.unlink() # unlink() deletes the file

            except PermissionError:
                print(f"Could not delete {file}") # file is likely open elsewhere

    def _open_directory(self, directory: Path) -> None:
        """
        Open the output folder in Windows File Explorer after saving charts.

        Uses os.startfile() which is Windows-only, this is acceptable since
        the project targets Windows machines. On other platforms this would
        need to be replaced with subprocess calls to 'open' (macOS) or 'xdg-open' (Linux).

        Parameters
            directory : Path of the folder to open.
        """
        os.startfile(directory)