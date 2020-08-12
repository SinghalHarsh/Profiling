"""Common parts to all other modules, mainly utility functions."""
import imghdr
import os
from enum import Enum, unique
from urllib.parse import ParseResult, urlparse

import numpy as np
import pandas as pd


# Numeric columns will be considered CATEGORICAL if fewer than this many distinct
max_numeric_distinct_to_be_categorical = 10

# Text columns will be considered TEXT if more than this many distinct (CATEGORICAL otherwise)
max_text_distinct_to_be_categorical = 101 ## 101

# Text columns will be considered TEXT if more than this fraction are distinct
max_text_fraction_distinct_to_be_categorical = 0.3 ## .33


@unique
class Variable(Enum):
    """The possible types of variables in the Profiling Report."""

    TYPE_CAT = "CAT"
    """A categorical variable"""

    TYPE_BOOL = "BOOL"
    """A boolean variable"""

    TYPE_NUM = "NUM"
    """A numeric variable"""

    TYPE_DATE = "DATE"
    """A date variable"""
    
    TYPE_TEXT = "TEXT"
    
    TYPE_CONS = "CONSTANT"


    S_TYPE_UNSUPPORTED = "UNSUPPORTED"
    """An unsupported variable"""


def get_counts(series: pd.Series) -> dict:
    """Counts the values in a series (with and without NaN, distinct).
    Args:
        series: Series for which we want to calculate the values.
    Returns:
        A dictionary with the count values (with and without NaN, distinct).
    """
    value_counts_with_nan = series.value_counts(dropna=False)
    value_counts_without_nan = (
        value_counts_with_nan.reset_index().dropna().set_index("index").iloc[:, 0]
    )

    distinct_count_with_nan = value_counts_with_nan.count()
    distinct_count_without_nan = value_counts_without_nan.count()

    return {
        "value_counts": value_counts_without_nan,  # Alias
        "value_counts_with_nan": value_counts_with_nan,
        "value_counts_without_nan": value_counts_without_nan,
        "distinct_count_with_nan": distinct_count_with_nan,
        "distinct_count_without_nan": distinct_count_without_nan,
        "num_rows_with_data": series.count(),
        "num_rows_total": len(series),        
    }


def is_boolean(series: pd.Series, series_description: dict) -> bool:
    """Is the series boolean type?
    Args:
        series: Series
        series_description: Series description
    Returns:
        True is the series is boolean type in the broad sense (e.g. including yes/no, NaNs allowed).
    """
    keys = series_description["value_counts_without_nan"].keys()
    if pd.api.types.is_bool_dtype(keys):
        return True
    elif (
        1 <= series_description["distinct_count_without_nan"] <= 2
        and pd.api.types.is_numeric_dtype(series)
        and series[~series.isnull()].between(0, 1).all()
    ):
        return True
    elif 1 <= series_description["distinct_count_without_nan"] <= 4:
        unique_values = set([str(value).lower() for value in keys.values])
        accepted_combinations = [
            ["y", "n"],
            ["yes", "no"],
            ["true", "false"],
            ["t", "f"],
        ]

        if len(unique_values) == 2 and any(
            [unique_values == set(bools) for bools in accepted_combinations]
        ):
            return True

    return False


def is_numeric(series: pd.Series, series_description: dict) -> bool:
    """Is the series numeric type?
    Args:
        series: Series
        series_description: Series description
    Returns:
        True is the series is numeric type (NaNs allowed).
    """
    return pd.api.types.is_numeric_dtype(series) and (
        series_description["distinct_count_without_nan"]
        > max_numeric_distinct_to_be_categorical
        or any(np.inf == s or -np.inf == s for s in series)
    )


def is_categorical(series: pd.Series, series_description: dict) -> bool:
    keys = series_description["value_counts_without_nan"].keys()
    # TODO: CHECK THIS CASE ACTUALLY WORKS
    if pd.api.types.is_categorical_dtype(keys):
        return True
    elif pd.api.types.is_numeric_dtype(series) and \
            series_description["distinct_count_without_nan"] \
            <= max_numeric_distinct_to_be_categorical:
        return True
    else:
        if series_description["num_rows_with_data"] == 0:
            return False
        num_distinct = series_description["distinct_count_without_nan"]
        fraction_distinct = num_distinct / float(series_description["num_rows_with_data"])
        if fraction_distinct \
             > max_text_fraction_distinct_to_be_categorical:
            return False
        if num_distinct <= max_text_distinct_to_be_categorical:
            return True
    return False



def is_date(series) -> bool:
    """Is the variable of type datetime? Throws a warning if the series looks like a datetime, but is not typed as
    datetime64.
    Args:
        series: Series
    Returns:
        True if the variable is of type datetime.
    """
    is_date_value = pd.api.types.is_datetime64_dtype(series)

    return is_date_value


def get_var_type(series: pd.Series) -> dict:
    """Get the variable type of a series.
    Args:
        series: Series for which we want to infer the variable type.
    Returns:
        The series updated with the variable type included.
    """

    series_description = {}

    try:
        series_description = get_counts(series)

        # When the inferred type of the index is just "mixed" probably the types within the series are tuple, dict,
        # list and so on...
        if series_description[
            "value_counts_without_nan"
        ].index.inferred_type.startswith("mixed"):
            raise TypeError("Not supported mixed type")

        if series_description["distinct_count_without_nan"] == 0:
            # Empty
            var_type = Variable.S_TYPE_UNSUPPORTED
        elif series_description["distinct_count_without_nan"] == 1:
            # Empty
            var_type = Variable.TYPE_CONS
        elif is_boolean(series, series_description):
            var_type = Variable.TYPE_BOOL
        elif is_numeric(series, series_description):
            var_type = Variable.TYPE_NUM
        elif is_date(series):
            var_type = Variable.TYPE_DATE
        elif is_categorical(series, series_description):
            var_type = Variable.TYPE_CAT
        else:
            var_type = Variable.TYPE_TEXT
    except TypeError:
        var_type = Variable.S_TYPE_UNSUPPORTED

    series_description.update({"type": var_type})

    return series_description



def get_df_var_types(df: pd.DataFrame) -> dict:
    
    var_types = {}
    
    for col_i in df.columns:
        var_types[col_i] = get_var_type(df[col_i])["type"].value
    
    return var_types


