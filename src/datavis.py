# Data Visualization

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time

import os
import shutil

import src.paths as paths

def datavis(N="TBD"):
    '''
    Create the heatmaps from .npy files containing the results from
    the classics that were run.
    '''
    print()
    print(f"Using {paths.PATH_DATA_CLEAN} as folder for input .npy files")
    print(f"Using {paths.PATH_FIGURES} as folder for images")
    print(f"Using {paths.PATH_FIGURES_ARCHIVE} as folder for archived images")

   # Need this for row and column labels
    color_patterns = np.load(paths.PATH_DATA_CLEAN / "possible_pairs.npy")
    print(f"Using color patterns {color_patterns})

    # Read in "Classic" Wins
    classic_wins_df = pd.DataFrame(
        np.load(paths.PATH_DATA_CLEAN / "_classic.npy"),
        index=color_patterns,
        columns=color_patterns
    )
    # Read in "Classic" Ties
    classic_ties_df = pd.DataFrame(
        np.load(paths.PATH_DATA_CLEAN / "_classic_ties.npy"),
        index=color_patterns,
        columns=color_patterns
    )
    # Read in "Ron's" Winws
    ron_wins_df = pd.DataFrame(
        np.load(paths.PATH_DATA_CLEAN / "_ron.npy"),
        index=color_patterns,
        columns=color_patterns
    )
    # Read in "Ron's Ties"
    ron_ties_df = pd.DataFrame(
        np.load(paths.PATH_DATA_CLEAN / "_ron_ties.npy"),
        index=color_patterns,
        columns=color_patterns
    )

    # Create the contents of the heatmap 
    # for the "Classic" game
    classic_annotations_df = (
        classic_wins_df.astype(str)
        + "\n"
        + "("
        + classic_ties_df.astype(str)
        + ")"
    )
    # Blank the diagonal of the dataframe
    for i in range(classic_annotations_df.shape[0]):
        classic_annotations_df.iloc[i,i] = " "

    # Create the contents of the heatmap 
    # for "Ron's" game
    ron_annotations_df = (
        ron_wins_df.astype(str)
        + "\n"
        + "("
        + ron_ties_df.astype(str)
        + ")"
    )
    # Blank the diagonal of the dataframe
    for i in range(ron_annotations_df.shape[0]):
        ron_annotations_df.iloc[i,i] = " "

    
    # Create a mask that can be used for both heatmaps
    # A mask is essentially a dataframe, that contains only True or False.
    # For the heatmap:
    # - True means hide / exclude this cell from the normal heatmap coloring
    # - False means show this cell normally
    
    # The heatmap then uses that mask to know which cells should not be drawn 
    # using the normal "Blues" colormap scale.
    
    # Copy dataframe to keep column and row names, and structure
    mask_df = classic_wins_df.copy()
    # Change columns from int64 to boolean
    mask_df = mask_df.astype('bool')
    # Set all cells to False
    mask_df[:] = False
    # Set the diagonal of the mask dataframe to True
    # in order to set it to light gray in the heatmap
    for i in range(mask_df.shape[0]):
        mask_df.iloc[i,i] = True

    # Obtain a colormap
    colormap = mpl.colormaps["Blues"]
    # Set the color for cells that are set to True
    # This is needed to have the diagonal be a light gray
    colormap.set_bad("lightgray")

    # Plot Heatmap(s)
    # Use one figure with two axes
    # first axes is for the "Classic" version
    # second axes is for "Ron's" version 
    fig, axes = plt.subplots(1, 2, figsize=(24, 12))
    plt.subplots_adjust(wspace=0.5)
    
    # classic_wins_df provides the structure of the heatmap:
    #    - Number of rows and columns
    #    - Row and column labels
    #    - Numeric values used to determine the cell colors
    #    - Values used by the color bar (cbar=True)
    
    # classic_annotations_df is yet another dataframe that provides the text 
    # annotations to be displayed inside each cell.
       
    # Create a heatmap for "Classic" version
    # Use dataframe classic_wins_df for the numeric heatmap values
    # Use dataframe classic annotations_df for the contents of the cells in the heatmap
    # Use colormap created 
    sns.heatmap(
        classic_wins_df,
        annot=classic_annotations_df,
        mask=mask_df,
        fmt="",
        cmap=colormap,
        linewidths=0.75,
        linecolor="white",
        cbar=False,
        ax=axes[0]
    )
    

    # Add a title
    title_string = (
        "My Probability of Win(Tie)\n"
        "Classic Scoring by [Tricks]\n"
        f"N={N}"
    )
    axes[0].set_title(title_string)
    
    # Label for columns
    axes[0].set_xlabel("My Choice")
    # Label for rows
    axes[0].set_ylabel("Opponent Choice")
    
    # Set the x-axis column labels
    # These are for "My Choice" and for "Opponent Choice"
    axes[0].set(xticklabels=color_patterns)
    axes[0].set(yticklabels=color_patterns)
        
    # Place row label at left of matrix
    axes[0].yaxis.set_label_position('left')
    # Place columns label at bottom of matrix
    axes[0].xaxis.set_label_position('bottom')
        
    # Hide the axis tick marks.
    # Display the column tick marks at the bottom
    # Display the row tick marks at the left
    # instead of at the bottom.
    axes[0].tick_params(
        which='both',
        bottom=False,
        left=True,
        labelbottom=True,
        labeltop=False)

    # ron_wins_df provides the structure of the heatmap:
    #    - Number of rows and columns
    #    - Row and column labels
    #    - Numeric values used to determine the cell colors
    #    - Values used by the color bar (cbar=True)
    
    # ron_annotations_df is yet another dataframe that provides the text 
    # annotations to be displayed inside each cell.
       
    # Create a heatmap for "Ron's" version
    # Use dataframe ron_wins_df for the numeric heatmap values
    # Use dataframe ron_annotations_df for the contents of the cells in the heatmap
    # Use colormap created 
    sns.heatmap(
        ron_wins_df,
        annot=ron_annotations_df,
        mask=mask_df,
        fmt="",
        cmap=colormap,
        linewidths=0.75,
        linecolor="white",
        cbar=False,
        ax=axes[1]
    )
    title_string = (
        "My Probability of Win(Tie)\n"
        "Ron's Scoring by [Cards]\n"
        f"N={N}"
    )
    
    axes[1].set_title(title_string)
    
    axes[1].set_xlabel("My Choice")
    axes[1].set_ylabel("Opponent Choice")
    
    axes[1].set(xticklabels=color_patterns)
    axes[1].set(yticklabels=color_patterns)
    
    axes[1].yaxis.set_label_position('left')
    axes[1].xaxis.set_label_position('bottom')

    # Hide the axis tick marks.
    # Display the column tick marks at the bottom
    # Display the row tick marks at the left
    # instead of at the bottom.
    axes[1].tick_params(
        which='both',
        bottom=False,
        left=True,
        labelbottom=True,
        labeltop=False)
    
    plt.tight_layout()

    # List all files currently in figures
    # There should be just one
    allfiles = os.listdir(paths.PATH_FIGURES)
    
    # Iterate thru files to move them to destination folder
    for f in allfiles:
        src_path = os.path.join(paths.PATH_FIGURES, f)
        # If its a file move it
        if os.path.isfile(src_path):
            dst_path = os.path.join(paths.PATH_FIGURES_ARCHIVE, f)
            shutil.move(src_path, dst_path)
        
    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    
    # Convert datetime obj to string
    str_current_datetime = str(current_datetime)
    # Remove "-" and replace " "
    str_current_datetime = str_current_datetime .replace("-", "").replace(" ", "_")
    
    # create a file object along with extension
    image_name = "Pennys_Game_" + str_current_datetime + ".png"
    print(f"Saving heatmap image {image_name}")
    
    # Save the heatmap as a PNG file
    plt.savefig(paths.PATH_FIGURES / image_name)
    
    plt.show()

    return