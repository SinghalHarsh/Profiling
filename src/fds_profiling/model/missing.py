import numpy as np
import pandas as pd

import seaborn as sns
sns.set_style("darkgrid")

from missingno import missingno

import matplotlib.pyplot as plt
from matplotlib import rcParams

from fds_profiling.visualisation.image_encoding import hex_to_rgb, plot_360_n0sc0pe

def missing_matrix(data: pd.DataFrame) -> str:
    """Generate missing values matrix plot
    Args:
      data: Pandas DataFrame to generate missing values matrix from.
    Returns:
      The resulting missing values matrix encoded as a string.
    """
    labels = True
    missingno.matrix(
        data,
        figsize=(10, 4),
        color=hex_to_rgb("#337ab7"),
        fontsize=10,
        sparkline=False,
        labels=labels,
    )
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)


def missing_count_column_wise(df):
    rcParams['figure.figsize'] = 10, 4

    dataframe = df

    row_count = dataframe.shape[0]

    ## missing: column wise
    missing_column_df = dataframe.isnull().sum()
    missing_column_df = pd.DataFrame(missing_column_df, columns=["Missing values"])
    
    missing_column_df["values"] = row_count
    missing_column_df = missing_column_df.apply(lambda x: 100*round(x/row_count, 2)).astype(int)
    missing_column_df.sort_values("Missing values", ascending=False, inplace=True)
    
    
    ## bar plot
    sns.set_style("darkgrid")
    ## plot 1 - "total" - (top) series
    sns.barplot(x=missing_column_df.index, y="values", data=missing_column_df, color="#337ab7", label="Values")

    ## plot 2 - overlay - "bottom" series
    sns.barplot(x=missing_column_df.index, y="Missing values", data=missing_column_df, color="red", label="Missing")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xticks(rotation="90")
    plt.ylabel('(%)', fontsize='12')
    plt.title("Missing values % in each column",weight="bold").set_fontsize('12')
    plt.tight_layout()
    return plot_360_n0sc0pe(plt)

def missing_count_row_wise(df):
    rcParams['figure.figsize'] = 10, 4

    dataframe = df

    # def missing_count_row_wise(dataframe)

    dataframe = df
    column_count = len(df.columns)

    row_count = dataframe.shape[0]

    ## missing: column wise
    missing_row_df = pd.DataFrame(dataframe.isnull().sum(axis=1).value_counts(), columns=["Number of rows"]).reset_index()

    missing_row_df["percent"] = missing_row_df["index"].apply(lambda x: 100*round(x/column_count, 2)).astype(int)
    missing_row_df["Missing cells %"] = missing_row_df.apply(lambda x: str(x["index"]) + " (" + str(x["percent"]) + "%)", axis=1)

    missing_row_df.sort_values("index", ascending=False, inplace=True)
    
    sns.barplot(x="Number of rows", y="Missing cells %", data=missing_row_df, orient="h", color="#337ab7")
    
    plt.xlabel('Number of rows', fontsize='12')
    plt.ylabel('Number of missing cells', fontsize='12')
#     plt.title("Missing values % in each column",weight="bold", fontsize='15')
    plt.tight_layout(rect=(0.1, 0, 0.9, 1))
    return plot_360_n0sc0pe(plt)
    
    
    
    

