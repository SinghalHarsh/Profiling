from fds_profiling.report import templates, renderable
from fds_profiling.model import missing


def missing_html(dataframe, anchor_id):
    
    ## reading template
    nav_table_template = templates.template("navigation_table.html")
    
    ## 1. column wise
    missing_count_column_wise_encoding = missing.missing_count_column_wise(dataframe)
    ## 2. row wise
    missing_count_row_wise_encoding = missing.missing_count_row_wise(dataframe)
    ## 3. missing matrix
    missing_matrix_encoding = missing.missing_matrix(dataframe)
    
    tabs = []
    
    tabs.append(
        renderable.Renderable(
            content = {
                "image_encoding": missing_matrix_encoding
            },
            name = "Matrix",
            anchor_id = anchor_id + "column",
            type_id = "image"))
    
    tabs.append(
        renderable.Renderable(
            content = {
                "image_encoding": missing_count_column_wise_encoding
            },
            name = "Column",
            anchor_id = anchor_id + "row",
            type_id = "image"))
    
    tabs.append(
        renderable.Renderable(
            content = {
                "image_encoding": missing_count_row_wise_encoding
            },
            name = "Row",
            anchor_id = anchor_id + "matrix",
            type_id = "image"))
        
    return nav_table_template.render(tabs = tabs, anchor_id = anchor_id)
        
            
