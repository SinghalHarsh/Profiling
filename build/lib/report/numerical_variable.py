import pandas as pd

from fds_profiling.report import templates, renderable
from fds_profiling.model.aggregators import groupby_aggregator, count_metric
from fds_profiling.visualisation.charts import *
from fds_profiling.model.describe import describe_series
from fds_profiling.model.associations import associations


def continuous_variable_html(df, col_name, metrics, anchor_id, target_var, var_types, assn_df):
    
    if (target_var != None):
        target_var_type = var_types[target_var]
    
    
    tabs = []
        
    ## 1ST TAB - statistics
    describe_df = describe_series(df[col_name], "NUM")
    
    tabs.append(
        renderable.Renderable(
            content = {
                "size": 3,
                "headings": ["Descriptive", "Variability", "Moments", "Outliers"],
                "contents": describe_df[0:4]},
            name = "Statistics",
            anchor_id = anchor_id + col_name + "statistics",
            type_id = "multiple_tables"))
            
    ## 2ND TAB - associations
    num_assn = assn_df[(assn_df["col_a"] == col_name) & (assn_df["type_"] == "NUM-NUM")]
    pos_num_assn = num_assn[num_assn['association'] >= 0.01].head(5)
    neg_num_assn = num_assn[num_assn['association'] <= -1*0.01].sort_values('association').head(5)

    cat_assn = assn_df[(assn_df["col_a"] == col_name) & (assn_df["type_"] == "NUM-CAT")]
    cat_assn = cat_assn[cat_assn["association"] > 0.01].head(5)

    table_pos_num_assn = convert_df_to_table(pos_num_assn, "col_b", "association")
    table_neg_num_assn = convert_df_to_table(neg_num_assn, "col_b", "association")
    table_cat_assn = convert_df_to_table(cat_assn, "col_b", "association")
            
    tabs.append(
        renderable.Renderable(
            content = {
                "size": 4,
                "headings": ["Positive correlation", "Negative correlation", "Categorical"],
                "contents": [table_pos_num_assn, table_neg_num_assn, table_cat_assn]
            },
            name = "Associations",
            anchor_id = anchor_id + col_name + "associations",
            type_id = "multiple_tables"))
            
    ## 3RD TAB - histogram
            
    ## a.Quantile ststistics
    quantile_df = describe_df[-1]
            
    ## b. Histogram
    histogram_encoding = histogram(df[col_name], col_name)
    
    tabs.append(
        renderable.Renderable(
            content = {"table_heading": "Quantile statistics", "table_content": quantile_df, "image_encoding": histogram_encoding},
            name = "Histogram",
            anchor_id = anchor_id + col_name + "histogram",
            type_id = "table_chart"))
    
    # 4TH TAB - target variable
            
    ## case 1: target column - CAT (bar chart)
    if ((target_var != None) and (target_var != col_name) and (target_var_type in ["CAT", "BOOL"])):
        
        ## a. table
        target_df = df[[col_name, target_var]]
        mean_df = target_df.groupby(target_var, as_index=False)[col_name].mean().sort_values(col_name, ascending=False)

        if (mean_df.shape[0] > 10):
            top_categories = list(mean_df[target_var][0:9])
            target_df.loc[~target_df[target_var].isin(top_categories), target_var] = "Others"
            mean_df = target_df.groupby(target_var, as_index=False)[col_name].mean().sort_values(col_name, ascending=False)
        
        ## renaming column
        mean_df.rename(columns={col_name:col_name + " (mean)"}, inplace=True)
       
        ## b. boxplot
        boxplot_encoding = boxplot(df[[col_name, target_var]], cat=target_var, num=col_name)
        
        tabs.append(
            renderable.Renderable(
                content = {"dataframe": mean_df.set_index(target_var), "image_encoding": boxplot_encoding, "df_size":3, "img_size":9},
                name = "Target Variable",
                anchor_id = anchor_id + col_name + "target_variable",
                type_id = "dataframe_chart"))
        
        
    ## case 2: target column - NUM (scatter chart)
    if ((target_var != None) and (target_var != col_name) and (target_var_type == "NUM")):
        
        stackbarchart_encoding = scatterplot(df[[col_name, target_var]], col_name, target_var)
        tabs.append(
            renderable.Renderable(
                content = {"image_encoding": stackbarchart_encoding},
                name = "Target Variable",
                anchor_id = anchor_id + col_name + "target_variable",
                type_id = "image"))
    
    
    
    
        
    return tabs


def convert_df_to_table(dataframe, name, value):
    
    table = []
    for index, row in dataframe.iterrows():
        table.append(
            { "name": row[name], "value": row[value], "alert": False },
        )
    return table
        
            
