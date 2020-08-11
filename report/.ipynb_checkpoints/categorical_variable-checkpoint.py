import pandas as pd
from fds_profiling.report import renderable
from fds_profiling.model.aggregators import groupby_aggregator, count_metric
from fds_profiling.visualisation.charts import *
from fds_profiling.model.describe import describe_series



def categorical_variable_html(df, col_name, metrics, anchor_id, target_var, var_types, assn_df):
        
    if (target_var != None):
        target_var_type = var_types[target_var]
    
    tabs = []
    
    # 1ST TAB - statistics
    describe_df = describe_series(df[col_name], "CAT")
    
    tabs.append(
        renderable.Renderable(
            content = { "size": 3, "headings": ["Descriptive"], "contents": describe_df},
            name = "Statistics",
            anchor_id = anchor_id + col_name + "statistics",
            type_id = "multiple_tables"))
    
            
    # 2ND TAB - associations
    cont_assn = assn_df[(assn_df["col_a"] == col_name) & (assn_df["type_"] == "CAT-NUM")]
    cont_assn = cont_assn[cont_assn['association'] >= 0.01].head(5)
    
    parent_assn = assn_df[(assn_df["col_a"] == col_name) & (assn_df["type_"] == "CAT-CAT")]
    parent_assn = parent_assn[parent_assn['association'] >= 0.01].head(5)
    
    child_assn = assn_df[(assn_df["col_b"] == col_name) & (assn_df["type_"] == "CAT-CAT")]
    child_assn = child_assn[child_assn['association'] >= 0.01].head(5)

    table_cont_assn = convert_df_to_table(cont_assn, "col_b", "association")
    table_parent_assn = convert_df_to_table(parent_assn, "col_b", "association")
    table_child_assn = convert_df_to_table(child_assn, "col_a", "association")
            
    tabs.append(
        renderable.Renderable(
            content = {
                "size": 4,
                "headings": ["Numerical", "Categorical (Can be inferred from)", "Categorical (Can be inferred about)"],
                "contents": [table_cont_assn, table_parent_assn, table_child_assn]
            },
            name = "Associations",
            anchor_id = anchor_id + col_name + "associations",
            type_id = "multiple_tables"))    
            
            
    # 3RD TAB - count

    ## a. table
    count_df = count_metric(df[col_name], col_name)    
    
    ## b. bar chart
    barchart_encoding = barchart(count_df, "Percent(%)", is_percent=True)
    
    tabs.append(
        renderable.Renderable(
            content = {"dataframe": count_df, "image_encoding": barchart_encoding, "df_size":6, "img_size":6},
            name = "Count",
            anchor_id = anchor_id + col_name + "Count",
            type_id = "dataframe_chart"))
    
            
    # 4TH TAB - target variable
            
    ## case 1: target column - NUM (bar chart)
    if ((target_var != None) and (target_var != col_name) and (target_var_type == "NUM")):
        
        ## a. table
        target_df = df[[col_name, target_var]]
        mean_df = target_df.groupby(col_name, as_index=False)[target_var].mean().sort_values(target_var, ascending=False)

        if (mean_df.shape[0] > 10):
            top_categories = list(mean_df[col_name][0:9])
            target_df.loc[~target_df[col_name].isin(top_categories), col_name] = "Others"
            mean_df = target_df.groupby(col_name, as_index=False)[target_var].mean().sort_values(target_var, ascending=False)
       
        ## b. boxplot
        boxplot_encoding = boxplot(df[[col_name, target_var]], cat=col_name, num=target_var)
        
        tabs.append(
            renderable.Renderable(
                content = {"dataframe": mean_df.set_index(col_name), "image_encoding": boxplot_encoding, "df_size":3, "img_size":9},
                name = "Target Variable",
                anchor_id = anchor_id + col_name + "target_variable",
                type_id = "dataframe_chart"))
        
        
    ## case 2: target column - CAT (100% stack chart)
    if ((target_var != None) and (target_var != col_name) and (target_var_type in ["CAT", "BOOL"])):
        
        stackbarchart_encoding = stackbarchart(df[[col_name, target_var]], col_name, target_var)
        tabs.append(
            renderable.Renderable(
                content = {"image_encoding": stackbarchart_encoding},
                name = "Target Variable",
                anchor_id = anchor_id + col_name + "target_variable",
                type_id = "image"))
            
            
    ## REMAINING TABS - user metrics
    
    if (len(metrics) > 0):
        
        ## groupby data
        agg_df = groupby_aggregator(df, col_name, metrics)
        
        for metric_i in metrics:
            
            ## a. table: sorting and re-ordering
            temp_df = agg_df.sort_values(metric_i[0], ascending=False).head(5)
#             temp_df = temp_df[[metric_i[0]] + [col for col in temp_df if col != metric_i[0]]]
            
            ## b. bar chart:
            barchart_encoding = barchart(temp_df, metric_i[0])
            
            tabs.append(
                renderable.Renderable(
                    content = {"dataframe": temp_df, "image_encoding": barchart_encoding, "df_size":6, "img_size":6},
                    name = metric_i[0],
                    anchor_id = anchor_id + col_name + metric_i[0].replace(" ", "_"),
                    type_id = "dataframe_chart"))
            
     
    return tabs


def convert_df_to_table(dataframe, name, value):
    
    table = []
    for index, row in dataframe.iterrows():
        table.append(
            { "name": row[name], "value": row[value], "alert": False },
        )
    return table
        
            
