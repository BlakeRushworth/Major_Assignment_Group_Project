# Major_Assignment_Group_Project
A console and GUI application for exploratory data analysis of stream macroinvertebrate images.
Built as part of Software Technology 1 (4483/8995), Group Assignment 3.
Team: Blake, Deacon, Ash

# Project Goal
This application allows users to select a subset of stream macroinvertebrate species from the Kaggle dataset, 
explore the image data through charts and statistics, and apply basic image transformations, all through either 
a console menu or a Tkinter GUI dashboard.

# Features 
- **Dataset validation**: checks the dataset exists at startup and guides the user to download it if not
- **Species selection**: choose all species or a custom subset (minimum 3) before any analysis runs
- **Dataset indexing**: scans the selected species folders and builds a DataFrame with file path, dimensions, and channel info per image
- **Dataset summary**: per-species image count, average dimensions, and file paths printed to console
- **Class distribution chart**: bar chart showing image counts across all selected species
- **Image size distribution**: histograms of pixel width and height, overall or per species
- **Sample image grid**: a 3×3 grid of randomly sampled images from the dataset
- **Brightness distribution**: histogram of mean greyscale brightness values across images
- **Image manipulation**: resize, greyscale, and invert transforms applied to one random image per species, saved to data/processed/

# Packages Used
- **Keras/Tensorflow**: Image loading and saving for manipulation functions
- **Opencv**: Image loading, decoding, and manipulation
- **Matplotlib**: Chart generation and image display
- **Pandas**: DataFrame construction and aggregation
- **Pathlib**: Cross-platform path handling
- **Numpy**: Array operations and fallback image decoding
- **Sys**: Provides a list of directories where Python looks for modules
- **Re**: Replaces occurrences of a pattern with a different string
- **Os**: File and Directory Management

# Installation
1. **Clone the repository** <br>
   |---- git clone https://github.com/BlakeRushworth/Major_Assignment_Group_Project <br>
   |---- cd Major_Assignment_Group_Project/GroupAssignment/macro_project
3. **Install dependencies** <br>
   |---- pip install -r requirements.txt
4. **Download the dataset** 
   - Go to https://www.kaggle.com/datasets/kennethtm/stream-macroinvertebrates
   - Click Download (free Kaggle account required)
   - Unzip the downloaded file
   - Move the extracted species folders into: <br>
     |---- data/raw/stream_macroinvertebrates/
   - The folder structure should look like: <br>
     |---- data/raw/stream_macroinvertebrates/ <br>
     |----|---- Asellus sp/ <br>
     |----|----|---- CPH-Asellus sp.-0-t.png <br>
     |----|----|---- CPH-Asellus sp.-1-t.png <br>
     |----|---- Baetidae sp/ <br>
     |----|----|---- CPH-Baetidae sp.-0-t.png <br>
     |----|----|---- ... 

# How to Run
**Stage 1: Console application (EDA + image manipulation)** <br>
|---- python -m src.main
- Validates the dataset, prompts species selection, then opens a menu-driven interface
- From the menu you can view the dataset summary, generate charts, and apply image manipulations

# Folder Structure
**macro_project**/ <br>
|---- data/ <br>
|----|---- processed/          ← manipulated images saved here <br>
|----|---- raw/ <br>
|----|----|---- stream_macroinvertebrates/   ← dataset goes here <br>
|---- outputs/ <br>
|----|---- eda/                ← saved charts and graphs <br>
|----|---- models/             ← model outputs (Stage 2) <br>
|---- src/ <br>
|----|---- config.py           ← all paths and settings <br>
|----|---- main.py             ← console app entry point <br>
|----|---- console_app.py      ← console menu logic <br>
|----|---- dataset_index.py    ← image scanning and DataFrame building <br>
|----|---- setup_check.py      ← dataset validation and species selection <br>
|----|----services/ <br>
|----|----|---- workflow_service.py             ← coordinates data pipeline <br>
|----|----|---- eda_service.py                  ← chart generation methods <br>
|----|----|---- image_manipulation_functions.py ← resize, greyscale, invert <br>
|---- gitignore <br>
|---- README.md <br>
|---- requirements.txt <br>



