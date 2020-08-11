from fds_profiling.report import templates
from fds_profiling.report.renderable import Renderable
from fds_profiling.config import config
from fds_profiling.model.variable_types import get_df_var_types
from fds_profiling.model.describe import describe_dataframe
from fds_profiling.config import config
from fds_profiling.model.associations import associations
from fds_profiling.visualisation.network import networkplot

import sys
sys.path.insert(0, '/Users/harsh/Desktop/DATA_SCIENCE/PandasProfiling/')


def profiling(dataframe, output_file="fds_profiling.html", user_metrics=[], title="FDS PROFILING", target_variable=None):
    
    metrics = user_metrics
    
    ## variable type identification
    config.config["var_types"] = get_df_var_types(dataframe)
    column_types = config.config["var_types"]
    categorical_columns = [i for i, j in column_types.items() if j=="CAT"]
    
#     ## target variable
#     if (target_variable != None):
#         if (column_types[target_variable] == "NUM"):
#             def target_sum(df):
#                 return df[target_variable].mean()
#             metrics.insert(0, ("Mean " + target_variable, target_sum))
#         ## TODO for other types
    
    
    ## associations df
    associations_df = associations(dataframe, config.config["var_types"])
    
    
    ## report
    sections = []

    ## section 1: Overview
    df_info = describe_dataframe(dataframe, config.config["var_types"])
    sections.append(
        Renderable(
            content = {
                "size": 6,
                "headings": ["Dataset statistics", "Variable types"],
                "contents": df_info
            },
            name="Overview",
            anchor_id="overview",
            type_id="multiple_tables"))

    ## section 2: Variables
    sections.append(
        Renderable(
            content = {
                "dataframe":dataframe,
                "metrics":metrics,
                "column_types":config.config["var_types"],
                "target_variable":target_variable,
                "associations_df": associations_df
            },
            name="Variables",
            anchor_id="variables",
            type_id="variables_container"))

    # section 3: Missing values
    sections.append(
        Renderable(
            content = {"dataframe":dataframe},
            name="Missing values",
            anchor_id="missing_values",
            type_id="missing_container"))
    
    # section 4: Association
    sections.append(
        Renderable(
            content = {"image_encoding": networkplot(config.config["var_types"], associations_df)},
            name="Associations",
            anchor_id="associations",
            type_id="image"))
    
#     # section 5: Interactions
#     tabs = []
#     for col_a in categorical_columns:
#         col_a_tabs = []
#         for col_b in categorical_columns:
            
#             crosstab_df = dataframe.groupby([col_a, col_b]).apply(lambda x: dataframe["Survived"].sum()).unstack()
#             col_a_tabs.append(
#                 Renderable(
#                     content = {"dataframe": crosstab_df},
#                     name = col_b,
#                     anchor_id = "crosstab" + col_a + col_b,
#                     type_id = "dataframe"))
    
#         tabs.append(
#             Renderable(
#                 content = {"tabs": col_a_tabs},
#                 name = col_a,
#                 anchor_id = "crosstab" + col_a,
#                 type_id = "interactions_container"))
        
#     sections.append(
#         Renderable(
#             content = {"tabs": tabs},
#             name = "Interactions",
#             anchor_id = "interactions",
#             type_id = "interactions_container"))
    

    
    
    ## creating HTML report
    
    ## reading template
    html_template = templates.template("report.html")

    ## navigations items
    nav_items = [ (section.name, section.anchor_id) for section in sections ]

    ##
    data = html_template.render(
        title = title,
        nav_items=nav_items,
        sections=sections
    )

    ## writing
    with open(output_file, "w") as file:
        file.write(data)
    
    
    
    
    