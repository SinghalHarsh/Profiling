import pandas as pd

from fds_profiling.report import templates, renderable
from fds_profiling.report.categorical_variable import categorical_variable_html
from fds_profiling.report.numerical_variable import continuous_variable_html
from fds_profiling.model.aggregators import groupby_aggregator, count_metric
from fds_profiling.visualisation.charts import *
from fds_profiling.model.describe import describe_series
from fds_profiling.model.associations import associations
from fds_profiling.visualisation.charts import wordcloud


def variables_html(dataframe, var_types, metrics, anchor_id, target_variable, associations_df):
    
    ## reading template
    nav_table_template = templates.template("navigation_table.html")
        
    html = ""
    
    for var_i, var_type in var_types.items():
        
        tabs = []
        
        if (var_type == "NUM"):
            tabs = continuous_variable_html(
                dataframe,
                var_i,
                metrics,
                anchor_id,
                target_variable,
                var_types,
                associations_df)
            
            
        elif ((var_type == "CAT") | (var_type == "BOOL")):
            tabs = categorical_variable_html(
                dataframe,
                var_i,
                metrics,
                anchor_id,
                target_variable,
                var_types,
                associations_df)
            
        else:
            ## 1ST TAB - statistics
            describe_df = describe_series(dataframe[var_i], var_type)
            tabs.append(
                renderable.Renderable(
                    content = {
                        "size": 3,
                        "headings": ["Descriptive", "Variability", "Moments", "Outliers"],
                        "contents": describe_df
                    },
                    name = "Statistics",
                    anchor_id = anchor_id + var_i + "statistics",
                    type_id = "multiple_tables"))
            
            if (var_type == "TEXT"):
            
                ## case 2: wordcloud
                wordcloud_encoding = wordcloud(dataframe[var_i])

                tabs.append(
                    renderable.Renderable(
                        content = {"image_encoding": wordcloud_encoding},
                        name = "Word cloud",
                        anchor_id = anchor_id + var_i + "wordcloud",
                        type_id = "image"))

        
        html += nav_table_template.render(tabs = tabs, anchor_id = anchor_id, header=var_i, sub_heading=var_type)
        
        
        
    return html


def convert_df_to_table(dataframe, name, value):
    
    table = []
    for index, row in dataframe.iterrows():
        table.append(
            { "name": row[name], "value": row[value], "alert": False },
        )
    return table
        
            
