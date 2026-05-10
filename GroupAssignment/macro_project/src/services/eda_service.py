from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
class EDAService:
    """Generate and save EDA outputs for the indexed image dataset."""
    
    def __init__(self, dataframe: pd.DataFrame, output_dir: Path) -> None:
        self.dataframe = dataframe
        self.output_dir = output_dir

    def save_class_distribution(self) -> None:
        """Save a class-count chart for the dataset."""

        plt.figure(figsize=(12, 6))
        order = self.dataframe["label"].value_counts().index
        sns.countplot(data=self.dataframe, x="label", order=order)
        plt.xticks(rotation=90)
        plt.title("Macroinvertebrate Images per Class")
        plt.tight_layout()
        plt.savefig(self.output_dir / "class_distribution.png")
        plt.close()
    
    def save_image_size_distribution(self) -> None:
        """Save width and height distribution charts."""
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

    def build_summary(self) -> dict[str, float]:
        """Return key dataset summary statistics."""

        return {
        "total_images": int(len(self.dataframe)),
        "total_classes": int(self.dataframe["label"].nunique()),
        "mean_width": float(self.dataframe["width"].mean()),
        "mean_height": float(self.dataframe["height"].mean()),
        }