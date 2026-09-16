# Data Visualization

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

import src.paths as paths

def datavis(input_file="datavis_test_input.csv"):
    '''
    Create the heatmap from .csv file containing the results from
    the simulations that were run.
    '''

    print(f"Using {paths.PATH_DATA_CLEAN} as folder for input .csv file")
    print(f"Using {input_file} as the input .csv file")
    print(f"Using {paths.PATH_FIGURES} as folder for heatmap file")

    # Read in .csv file and build dataframe
    results_df = pd.read_csv(
        paths.PATH_DATA_CLEAN / input_file,
        dtype=str
    )

    # Reformat the dataframe
    results_df = results_df.set_index(results_df.columns[0])
    results_df.index.name = None
    print("Results dataframe from input file")
    print(results_df)
    
    def extract_wins(cell):
        '''
        Extract the wins as numeric from the tuple in each cell of the 
        results_df. The heatmap must have numeric values in each cell
        of the input dataframe in order to determine the colors to 
        be used.
        '''
        first, second = cell.strip("()").split(",")
        wins = int(first)
        return wins
        
    # Obtain the wins in numeric format
    # using the extract_wins function
    # Place in new dataframe simulation_wins_df
    # this will be used by heatmap
    simulation_wins_df = results_df.map(extract_wins)

    # Create a new dataframe, "annotations_df", from results_df
    # It will be used by sns.heatmap() for what text 
    # to display inside each cell of the heatmap.
    # 
    # Convert the tuple in the cells found in results_df 
    # that contains "(wins,ties)" to a string that has "wins(ties)"
    # For example: (76,7) which is 76 wins and 7 ties
    # would be reformat to 76(7) place the ties in paren
    # to each cell
    def reformat_cell(cell):
        '''
        Reformat the cells from the results which are in tuple format
        "(wins,ties)" to "wins(ties)"
        This is due to Ron's heatmap formatting reqs.
        '''
        first, second = cell.strip("()").split(",")
        s = f"{first}\n({second})"
        return s

    annotations_df = results_df.map(reformat_cell)

    print("After reformatting results for use in heatmap")
    print(annotations_df)
   
    # Blank the diagonal of the dataframe
    # to comply with Ron's requirement
    for i in range(annotations_df.shape[0]):
        annotations_df.iloc[i,i] = " "

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


    # Plot Heatmap
    plt.figure(figsize=(10, 10))
    
    # simulation_wins_df provides the structure of the heatmap:
    #    - Number of rows and columns
    #    - Row and column labels
    #    - Numeric values used to determine the cell colors
    #    - Values used by the color bar (cbar=True)
    
    # annotations_df is yet another dataframe that provides the text 
    # annotations to be displayed inside each cell.
    
    # Obtain a colormap
    colormap = mpl.colormaps["Blues"]
    # Set the color for cells that are set to True
    # This is needed to have the diagonal be a light gray
    colormap.set_bad("lightgray")
    
    # Create a heatmap
    # Use dataframe simulation_wins_df for the structure
    # Use dataframe annotations_df for the contents of the cells in the heatmap
    # Use colormap created 
    ax = sns.heatmap(
        simulation_wins_df,
        annot=annotations_df,
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
    plt.savefig(paths.PATH_FIGURES / 'Pennys_Game.png')
    
    plt.show()

    return