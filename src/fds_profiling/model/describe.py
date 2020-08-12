import pandas as pd
from fds_profiling.model.summary import describe_numeric_1d, describe_categorical
from fds_profiling.model.summary import get_table_stats

def describe_dataframe(series: pd.Series, var_types: dict):
    
    ## Dataset statistics
    info = get_table_stats(series)
    
    overview = [
        { "name": "Number of variables", "value": info["n_var"], "alert": False},
        { "name": "Number of observations", "value": info["n"], "alert": False },
        { "name": "Missing cells", "value": str(info["n_cells_missing"]) + ' (' + str(info["p_cells_missing"]) + '%)', "alert": False },
        { "name": "Duplicate rows", "value": str(info["n_duplicated"]) + ' (' + str(info["p_duplicated"]) + '%)', "alert": False },
#         { "name": "Key columns", "value": "-", "alert": False }
    ]
    
    
    ## Variable types
    var_types_lst = [type_ for var, type_ in var_types.items()]
    var_types_count = dict((i, var_types_lst.count(i)) for i in var_types_lst)
    
    variable_types = []
    for type_, count_ in sorted(var_types_count.items()):
        variable_types.append(
            { "name": type_, "value": count_, "alert": False},
        )

    return [overview, variable_types]

def describe_series(series: pd.Series, column_type):
    
    if (column_type == "NUM"):
        
        info = describe_numeric_1d(series)
    
        descriptive = [
            { "name": "Values", "value": str(info["n_values"]) + ' (' + str(info["p_values"]) + '%)', "alert": False },
            { "name": "Missing", "value": str(info["n_missing"]) + ' (' + str(info["p_missing"]) + '%)', "alert": False },
            { "name": "Distinct count", "value": info["distinct_count"], "alert": False},
            { "name": "Zeros", "value": str(info["n_zeros"]) + ' (' + str(info["p_zeros"]) + '%)', "alert": False },
            { "name": "Min - Max", "value": str(info["min"]) + ' - ' + str(info["max"]), "alert": False }
        ]

        variability = [
            { "name": "Range", "value": info["range"], "alert": False },
            { "name": "Interquartile range (IQR)", "value": info["iqr"], "alert": False },
            { "name": "Variance", "value": info["variance"], "alert": False },
            { "name": "Standard deviation", "value": info["std"], "alert": False },
            { "name": "Median Absolute Deviation (MAD)", "value": info["mad"], "alert": False }
        ]

        moments = [
            { "name": "Mean", "value": info["mean"], "alert": False },
            { "name": "Median", "value": info["50%"], "alert": False },
            { "name": "Skewness", "value": info["skewness"], "alert": False },
            { "name": "Kurtosis", "value": info["kurtosis"], "alert": False }
        ]

        outlier = [
            { "name": "Outliers", "value": str(info["n_outlier"]) + ' (' + str(info["p_outlier"]) + '%)', "alert": False },
            { "name": "Top outliers", "value": str(info["n_outlier_top"]) + ' (' + str(info["p_outlier_top"]) + '%)', "alert": False },
            { "name": "Bottom outliers", "value": str(info["n_outlier_bottom"]) + ' (' + str(info["p_outlier_bottom"]) + '%)', "alert": False }
        ]
        
        quantile = [
            { "name": "Minimum", "value": info["min"], "alert": False },
            { "name": "5%", "value": info["5%"], "alert": False },
            { "name": "Q1", "value": info["25%"], "alert": False },
            { "name": "Median", "value": info["50%"], "alert": False },
            { "name": "Q3", "value": info["75%"], "alert": False },
            { "name": "95%", "value": info["95%"], "alert": False },
            { "name": "Maximum", "value": info["max"], "alert": False }
            
        ]
    
        return [descriptive, variability, moments, outlier, quantile]
    
    elif (column_type != "NUM"):
        
        info = describe_categorical(series)
        
        descriptive = [
            { "name": "Values", "value": str(info["n_values"]) + ' (' + str(info["p_values"]) + '%)', "alert": False },
            { "name": "Missing", "value": str(info["n_missing"]) + ' (' + str(info["p_missing"]) + '%)', "alert": False },
            { "name": "Distinct count", "value": info["distinct_count"], "alert": False},
            { "name": "Mode", "value": info["mode"], "alert": False }
        ]
    
        return [descriptive]
        
    else:
        pass