# coding=utf-8
import pandas as pd
import os

"""
.. module:: file_parser_mem.bed
"""


def parse_bed(filename, cache=0, cache_suffix="_pd_cache.csv"):
    STANDARD_FIELDS = ("chrom", "chromStart", "chromEnd", "name", "score", "strand",
                       "thickStart", "thickEnd", "itemRgb", "blockCount", "blockSizes", "blockStarts")
    if cache and os.path.exists(filename + cache_suffix):
        df = pd.read_csv(filename + cache_suffix, index_col=None, header=None)
    else:
        try:
            # canonical bed format, no track line
            df = pd.read_csv(filename, sep="\t", header=None, comment="#")
        except pd.errors.ParserError:
            try:
                # with track line
                df = pd.read_csv(filename, sep="\t", header=None, comment="#", skiprows=1)
            except pd.errors.ParserError:
                # with data lines and track line
                df = pd.read_csv(filename, sep="\t", header=None, comment="#", skiprows=3)
    df[1] = df[1].astype(int)
    df[2] = df[2].astype(int)
    col_names = []
    n_sf = len(STANDARD_FIELDS)
    for i in range(df.shape[1]):
        if i < n_sf:
            col_names.append(STANDARD_FIELDS[i])
        else:
            col_names.append("NSF_{col}".format(col=i-n_sf))
    df.columns = col_names
    if cache:
        df.to_csv(filename + cache_suffix, index=False, header=False)
    return df
