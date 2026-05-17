from pathlib import Path
import os
import matplotlib.pyplot as plt
import cv2
import pandas as pd
import seaborn as sns
class EDAService:
    """Generate and save EDA outputs for the indexed image dataset."""
    
    def __init__(
        self,
        dataframe: pd.DataFrame,
        output_dir: Path
    ) -> None:

        self.dataframe = dataframe
        self.output_dir = output_dir

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_class_distribution(self) -> None:
        """Save a class-count chart for the dataset."""
        print("[System] Creating Graphs...")
        base_dir = self.output_dir / "class_distribution_charts"
        base_dir.mkdir(parents=True, exist_ok=True)
        self._clear_png_files(base_dir)
        plt.figure(figsize=(12, 6))
        order = self.dataframe["species"].value_counts().index
        sns.countplot(data=self.dataframe, x="species", order=order)
        plt.xticks(rotation=90)
        plt.title("Macroinvertebrate Images per Class")
        plt.tight_layout()
        plt.savefig(base_dir / "class_distribution.png")
        self._open_directory(base_dir)
        plt.close()
    
    def save_image_size_distribution(self,per_species: bool = False) -> None:
        """Save width and height distribution charts."""
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
        """Save a grid of sample dataset images."""
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
        """Save brightness distribution graph."""
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
        """Save width versus height scatter plot."""
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
        """Save width boxplot."""
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

            plt.xticks(rotation=45)

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
        """Save height boxplot."""
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

            plt.xticks(rotation=45)

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
        """Save grayscale pixel intensity histogram."""
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
        """Return key dataset summary statistics."""

        return {
        "total_images": int(len(self.dataframe)),
        "total_classes": int(self.dataframe["species"].nunique()),
        "mean_width": float(self.dataframe["width"].mean()),
        "mean_height": float(self.dataframe["height"].mean()),
        }
    
    def _clear_png_files(self, directory: Path) -> None:
        """Delete old PNG files from a directory to keep clean."""

        for file in directory.glob("*.png"):

            try:
                file.unlink()

            except PermissionError:
                print(f"Could not delete {file}")

    def _open_directory(self, directory: Path) -> None:
        """Open folder in File Explorer."""
        os.startfile(directory)