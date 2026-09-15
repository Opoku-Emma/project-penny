# Data Visualization
import src.paths as paths

# Probably more complicated than it needs to be
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

def datavis(
    wins: pd.DataFrame,
    ties: pd.DataFrame
) -> None:

    # Currently written to use passed dataframes.
    # Will change to read in .csv files and convert to dataframes.
  
    # Currently uses the two dataframes that contain the wins and ties
    # Needs to be modified to still use two dataframes, but
    # the first one will contain the results of the classic game,
    # the second one will contain the results of Ron's game
    # It will also be changed to expect a tuple in each dataframe cell
    # This tuple will contain the # of wines and the # of ties

    # Current function
    simulation_wins_df = wins
    simulation_ties_df = ties

    # Create a new dataframe, "labels", from simulation_wins_df
    # It will be used by sns.heatmap() for what text 
    # to display inside each cell of the heatmap.
    # 
    # convert the wins to string
    # convert the ties to string
    # place the ties in paren
    # to each cell
    
    labels_df = (
        simulation_wins_df.astype(str)
        + "\n"
        + "("
        + simulation_ties_df.astype(str)
        + ")"
    )
    print(labels_df)
    
    # Blank the diagonal of the dataframe
    # to comply with Ron's requirement
    for i in range(labels_df.shape[0]):
        labels_df.iloc[i,i] = " "

    # Create a mask 
    # A mask is essentially a dataframe, that contains only True or False.
    # For the heatmap:
    # - True means hide / exclude this cell from the normal heatmap coloring
    # - False means show this cell normally
    
    # The heatmap then uses that mask to know which cells should not be drawn 
    # using the normal "Blues" colormap scale.
    
    # Copy dataframe to keep column and row names, and structure
    mask_df = simulation_wins_df.copy()
    # Change columns from int64 to boolean
    mask_df = mask_df.astype('bool')
    # Set all cells to False
    mask_df[:] = False
    # Set the diagonal of the mask dataframe to True
    # in order to set it to light gray in the heatmap
    for i in range(mask_df.shape[0]):
        mask_df.iloc[i,i] = True

    print(mask_df)
    # Plot Heatmap
    plt.figure(figsize=(10, 10))
    
    # simulation_wins_df provides the structure of the heatmap:
    #    - Number of rows and columns
    #    - Row and column labels
    #    - Numeric values used to determine the cell colors
    #    - Values used by the color bar (cbar=True)
    
    # labels is yet another dataframe that provides the text 
    # annotations to be displayed inside each cell.
    
    # Obtain a colormap
    colormap = mpl.colormaps["Blues"]
    # Set the color for cells that are set to True
    # This is needed to have the diagonal be a light gray
    colormap.set_bad("lightgray")
    
    # Create a heatmap
    # Use dataframe simulation_wins_df for the structure
    # Use dataframe label_df for the contents of the cells in the heatmap
    # Use colormap created 
    ax = sns.heatmap(
        simulation_wins_df,
        annot=labels_df,
        mask=mask_df,
        fmt="",
        cmap=colormap,
        linewidths=0.75,
        linecolor="white",
        cbar=False
    )
    
    # Add a title 
    title_string = 'My Probability of Win(Tie)' + '\n' + 'Scoring by [Cards/Tricks]'
    ax.set_title(title_string)
    
    # Label for columns
    ax.set_xlabel("My Choice")
    # Label for rows
    ax.set_ylabel("Opponent Choice")
    
    # Place columns label at bottom of matrix
    ax.xaxis.set_label_position('bottom')
    
    # Set the x-axis column labels
    # These are for "My Choice"
    ax.set(xticklabels = ([
        "RRR",
        "RRB",
        "RBR",
        "RBB",
        "BRR",
        "BRB",
        "BBR",
        "BBB"]))
    
    # Place row label at left of matrix
    ax.yaxis.set_label_position('left')
    
    # Set the y-axis column labels
    # These are for "Opponent Choice"
    ax.set(yticklabels = ([
        "RRR",
        "RRB",
        "RBR",
        "RBB",
        "BRR",
        "BRB",
        "BBR",
        "BBB"]))
    
    # Hide the axis tick marks.
    # Display the column tick marks at the bottom
    # Display the row tick marks at the left
    # instead of at the bottom.
    plt.tick_params(
        which='both',
        bottom=False,
        left=True,
        labelbottom=True,
        labeltop=False)
    
    plt.tight_layout()
    
    # Save the plot as a PNG file
    # Save it in the figures folder
    # Possibly use the 
    plt.savefig('figures/Pennys_Game.png')
    
    plt.show()

    return
