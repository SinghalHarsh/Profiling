import numpy as np
import pandas as pd

def get_table_stats(df: pd.DataFrame) -> dict:
    """
    General statistics for the DataFrame.
    """
    n = len(df)

    table_stats = {
        "n": n,
        "n_var": len(df.columns),
        "n_cells_missing": df.isnull().sum().sum(),
        "n_duplicated": sum(df.duplicated())
    }

    table_stats["p_cells_missing"] = 100*(table_stats["n_cells_missing"] / (table_stats["n"] * table_stats["n_var"]))
    table_stats["p_duplicated"] = 100*(table_stats["n_duplicated"] / (table_stats["n"] * table_stats["n_var"]))

    for key, value in table_stats.items():
        try:
            table_stats[key] = round(value, 2)
        except:pass
    return table_stats

def describe_numeric_1d(series: pd.Series) -> dict:
        
    def mad(arr):
        """ Median Absolute Deviation: a "Robust" version of standard deviation.
            Indices variability of the sample.
            https://en.wikipedia.org/wiki/Median_absolute_deviation
        """
        return np.median(np.abs(arr - np.median(arr)))
    
    stats = {}
                
    # number of observations in the Series
    stats["num_rows_total"] = len(series)

    # number of non-NaN observations in the Series
    stats["num_rows_with_data"] = series.count()
    
    # distinct count
    value_counts_with_nan = series.value_counts(dropna=False)
    value_counts_without_nan = series.value_counts(dropna=True)
    stats["distinct_count_with_nan"] = value_counts_with_nan.count()
    stats["distinct_count_without_nan"] = value_counts_without_nan.count()

    stats["distinct_count"] = stats["distinct_count_without_nan"]
    
    # values
    stats["n_values"] = stats["num_rows_with_data"]
    stats["p_values"] = 100*(stats["num_rows_with_data"] / stats["num_rows_total"])
    
    # missing
    stats["n_missing"] = stats["num_rows_total"] - stats["num_rows_with_data"]
    stats["p_missing"] = 100*(1 - (stats["num_rows_with_data"] / stats["num_rows_total"]))

    #
    stats["is_unique"] = stats["distinct_count_without_nan"] == stats["num_rows_with_data"]

    #
    values = series.values
    present_values = values[~np.isnan(values)]

    stats["mean"] = np.mean(present_values)
    stats["mode"] = series.mode().iloc[0] if stats["num_rows_with_data"] > stats["distinct_count_without_nan"] > 1 else series[0]
    
    stats["std"] = np.std(present_values, ddof=1)
    stats["variance"] = np.var(present_values, ddof=1)
    # Median Absolute Deviation 
    stats["mad"] = mad(present_values)
    
    stats["min"] = np.min(present_values)
    stats["max"] = np.max(present_values)
    stats["range"] = stats["max"] - stats["min"]
    
    # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
    stats["kurtosis"] = series.kurt()
    # Unbiased skew normalized by N-1
    stats["skewness"] = series.skew()
    
    
    # zeros
    stats["n_zeros"] = (stats["num_rows_with_data"] - np.count_nonzero(present_values))
    stats["p_zeros"] = 100*(stats["n_zeros"] / stats["num_rows_total"])
    
    # quantiles
    quantiles = [.05, .25, .5, .75, .95]
    stats.update(
        {
            f"{percentile:.0%}": value
            for percentile, value in series.quantile(quantiles).to_dict().items()
        }
    )
    stats["iqr"] = stats["75%"] - stats["25%"]
    
    # outliers
    stats["n_outlier_top"] = len(series[series > (stats["75%"] + 1.5*stats["iqr"])])
    stats["n_outlier_bottom"] = len(series[series < (stats["25%"] - 1.5*stats["iqr"])])
    stats["n_outlier"] = stats["n_outlier_top"] + stats["n_outlier_bottom"]
    
    stats["p_outlier_top"] = 100*(stats["n_outlier_top"] / stats["num_rows_total"])
    stats["p_outlier_bottom"] = 100*(stats["n_outlier_bottom"] / stats["num_rows_total"])
    stats["p_outlier"] = 100*(stats["n_outlier"] / stats["num_rows_total"])
    
    
    for key, value in stats.items():
        try:
            stats[key] = round(value, 2)
        except:pass
    return stats

def describe_categorical(series: pd.Series) -> dict:
    
    stats = {}
    
    # number of observations in the Series
    stats["num_rows_total"] = len(series)

    # number of non-NaN observations in the Series
    stats["num_rows_with_data"] = series.count()
                
    value_counts_with_nan = series.value_counts(dropna=False)
    value_counts_without_nan = series.value_counts(dropna=True)
    stats["distinct_count_with_nan"] = value_counts_with_nan.count()
    stats["distinct_count_without_nan"] = value_counts_without_nan.count()

    stats["distinct_count"] = stats["distinct_count_without_nan"]
    
    # values
    stats["n_values"] = stats["num_rows_with_data"]
    stats["p_values"] = 100*(stats["num_rows_with_data"] / stats["num_rows_total"])
    
    # missing
    stats["n_missing"] = stats["num_rows_total"] - stats["num_rows_with_data"]
    stats["p_missing"] = 100*(1 - (stats["num_rows_with_data"] / stats["num_rows_total"]))
    
    stats["is_unique"] = stats["distinct_count"] == stats["num_rows_with_data"]
    stats["mode"] = series.mode().iloc[0] if stats["num_rows_with_data"] > stats["distinct_count"] > 1 else series[0]
    
    for key, value in stats.items():
        try:
            stats[key] = round(value, 2)
        except:pass
    
    return stats
