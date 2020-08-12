import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch

from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

import seaborn as sns
sns.set_style("darkgrid")

from pkg_resources import resource_filename
# matplotlib.style.use(resource_filename(__name__, "pandas_profiling.mplstyle"))

from fds_profiling.visualisation.image_encoding import hex_to_rgb, plot_360_n0sc0pe

from matplotlib import rcParams


def barchart(dataframe, numerical_column, is_percent=False):
    """
    df: frequency table
    """
    
    rcParams['figure.figsize'] = 8, 5
    
    if (is_percent):
        ## removing the % sign
#         dataframe[numerical_column] = dataframe[numerical_column].str.rstrip('%').astype('float')
#         sns.barplot(x=numerical_column, y=dataframe.index, data=dataframe, orient="h", order=dataframe.index, color="#337ab7")
        dataframe.sort_values(numerical_column, ascending=True)[numerical_column].plot.barh(color="#337ab7")
#         plt.barh(dataframe.index.values, dataframe[numerical_column])
        plt.xlim(0, 100)
    else:
#         sns.barplot(x=numerical_column, y=dataframe.index, data=dataframe, orient="h", order=dataframe.index, color="#337ab7")
        dataframe.sort_values(numerical_column, ascending=True)[numerical_column].plot.barh(color="#337ab7")
#     df.plot.barh()
#     plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)

    plt.xticks(fontsize=12, rotation=0)
    plt.yticks(fontsize=12, rotation=0)
    plt.xlabel(numerical_column, fontsize=15)
    plt.ylabel(dataframe.index.name, fontsize=15)
#     plt.subplots_adjust(left=0.4, right=0.6, top=0.9, bottom=0.1)
    plt.tight_layout(rect=(0.1, 0.1, 0.9, 0.9))
    
    return plot_360_n0sc0pe(plt)


def histogram(series: pd.Series, col_name):
    
    ## drawing
    ## - fixing the size of the figure 
    rcParams['figure.figsize'] = 10, 5
    
    x = np.array(series.dropna())
    
    # Cut the window in 2 parts
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, 
                                    gridspec_kw={"height_ratios": (.15, .85)}
                                   )

    sns.boxplot(x, ax=ax_box, color="#337ab7")
    sns.distplot(x, ax=ax_hist, color="#337ab7")

    ax_box.set(yticks=[])
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)
    
    plt.xticks(fontsize=12, rotation=0)
    plt.yticks(fontsize=12, rotation=0)
    plt.tight_layout()
    return plot_360_n0sc0pe(plt)


def boxplot(df, num, cat):
    
    rcParams['figure.figsize'] = 10, 5
    
    temp_df = df[[num, cat]]
    sorted_order = temp_df.groupby(cat, as_index=False)[num].mean().sort_values(num, ascending=False)

    if (sorted_order.shape[0] > 10):
        top_categories = list(sorted_order[cat][0:9])
        temp_df.loc[~temp_df[cat].isin(top_categories), cat] = "Others"
        sns.boxplot(x=cat, y=num, data=temp_df, order = top_categories + ["Others"])

    else:
        sns.boxplot(x=cat, y=num, data=temp_df, order = sorted_order[cat])
        
    plt.xticks(fontsize=12, rotation=0)
    plt.yticks(fontsize=12, rotation=0)
    plt.xlabel(cat, fontsize=15)
    plt.ylabel(num, fontsize=15)
#     plt.subplots_adjust(left=0.4, right=0.6, top=0.9, bottom=0.1)
    plt.tight_layout(rect=(0.1, 0.1, 0.9, 0.9))
    
    return plot_360_n0sc0pe(plt)

def stackbarchart(df, cat_a, cat_b):
    
    rcParams['figure.figsize'] = (10, 4)

    ## keeping only top 10 categories
    temp_df = df[[cat_a, cat_b]]
    sorted_order = list(temp_df[cat_a].value_counts().index)

    if (df[cat_a].nunique() > 10):
        temp_df.loc[~temp_df[cat_a].isin(sorted_order[0:9]), cat_a] = "Others"
        sorted_order = sorted_order[0:9] + ["Others"]

    if (df[cat_b].nunique() > 10):
        top_categories = list(temp_df[cat_b].value_counts().index[0:9])
        temp_df.loc[~temp_df[cat_b].isin(top_categories), cat_b] = "Others" 

    ## plots
    fig, (ax1, ax2) = plt.subplots(1, 2)

    grouped_df = temp_df.groupby([cat_a, cat_b]).size()
    grouped_df.unstack().reindex(index=sorted_order).plot(kind='bar', stacked=True, ax = ax1, legend=False)
    ax1.set_title("Bar Chart",weight="bold").set_fontsize('12')

    cross_df = pd.crosstab(temp_df[cat_a], temp_df[cat_b]).apply(lambda r: r/r.sum(), axis=1)
    cross_df.reindex(index=sorted_order).plot(kind='bar', stacked=True, ax=ax2 )
    ax2.set_title("Stacked Chart",weight="bold").set_fontsize('12')
    
    ax2.legend(title=cat_b, loc='center left', bbox_to_anchor=(1, 0.5))
    
    
    plt.tight_layout(rect=(0.1, 0.05, 0.9, 0.95))
    return plot_360_n0sc0pe(plt)

def scatterplot(df, num_a, num_b):
    
    ## plots
    fig, (ax1, ax2) = plt.subplots(1, 2)

    sns.distplot( df[num_a].dropna() , color="skyblue", label=num_a, ax=ax1)
    sns.distplot( df[num_b].dropna() , color="red", label=num_b, ax=ax1)
    ax1.set_title("",weight="bold").set_fontsize('12')

    sns.regplot(df[num_a], df[num_b], ax=ax2)
    reg_coeff = round(df[num_a].corr(df[num_b]), 2)
    ax2.set_title("R: " + str(reg_coeff), weight="bold").set_fontsize('12')

    return plot_360_n0sc0pe(plt)

def wordcloud(series):
    
    stopwords = set(STOPWORDS)
    
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40, 
        random_state=42
    ).generate(str(series.values))

    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    return plot_360_n0sc0pe(plt)

