# coding=utf-8
# Original: Kamil Slowikowski
from collections import defaultdict
import gzip
import os
import pandas as pd

GTF_HEADER = ['seqname', 'source', 'feature', 'start', 'end', 'score',
              'strand', 'frame']


def parse_gtf(filename, cache=1, cache_suffix="_pd_cache.csv"):
    """
    Parse GTF file

    Parameters
    ----------
    filename : str
        path to plain GTF or gzipped GTF
    cache : bool or int
        1/True for generating cache
    cache_suffix : str
        suffix for the cached file

    Returns
    -------
    df : pd.DataFrame
        parsed gtf
    """
    assert os.path.exists(filename), "Cannot access the file you provided."
    from datetime import datetime

    if cache and os.path.exists(filename + cache_suffix):
        gtf_time = datetime.fromtimestamp(os.path.getctime(filename))
        cache_time = datetime.fromtimestamp(os.path.getctime(filename + cache_suffix))
        if cache_time >= gtf_time:  # only load from cache if the cache is newer than the gtf
            return pd.read_csv(filename + cache_suffix, index_col=None)

    result = defaultdict(list)

    for i, line in enumerate(read_lines(filename)):
        for key in line.keys():
            if key not in result:
                result[key] = [None] * i

        for key in result.keys():
            result[key].append(line.get(key, None))

    df = pd.DataFrame(result)
    if cache:
        df.to_csv(filename + cache_suffix, index=False)
    if not pd.api.types.is_numeric_dtype(df["start"]):
        df["start"] = df["start"].astype(int)
    if not pd.api.types.is_numeric_dtype(df["end"]):
        df["end"] = df["end"].astype(int)
    return df


def read_lines(filename):
    """Open an GTF file and generate a dict for each line.

    Parameters
    ----------
    filename : str
        path to the gtf file

    Returns
    -------
    yield
    """
    fn_open = gzip.open if filename.endswith('.gz') else open
    mode = "rt" if filename.endswith('.gz') else "r"

    with fn_open(filename, mode) as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            else:
                yield parse(line)


def parse(line):
    """Parse a single line from a GTF file and return a dict

    Parameters
    ----------
    line : str

    Returns
    -------
    line_elements : dict
        elements in this line
    """
    result = {}

    fields = line.rstrip().split('\t')

    for i, col in enumerate(GTF_HEADER):
        result[col] = _get_value(fields[i])

    # INFO field consists of "key1=value;key2=value;...".
    # infos = [x for x in re.split(R_SEMICOLON, fields[8]) if x.strip()]
    infos = [x for x in fields[8].split(";") if x.strip()]

    for i, info in enumerate(infos, 1):
        # It should be key="value".
        try:
            key, value = info.split()
        # But sometimes it is just "value".
        except ValueError:
            key = 'INFO{}'.format(i)
            value = info
        # Ignore the field if there is no value.
        if value:
            result[key] = _get_value(value)

    return result


def _get_value(value):
    """Get value of the key

    Parameters
    ----------
    value : str
        value

    Returns
    -------
    value : str or list
        Handled value
    """
    if not value:
        return None

    # Strip double and single quotes.
    value = value.strip('"\'')

    # Return a list if the value has a comma.
    if ',' in value:
        value = value.split(",")
    # These values are equivalent to None.
    elif value in ['', '.', 'NA']:
        return None

    return value


def write_gtf(df, save_to, fill_empty=False):
    """
    Write a dataframe to a gtf file

    Parameters
    ----------
    df : pd.DataFrame

    save_to : str

    fill_empty : bool
        Fill empty/missing values in GTF main cols

    Returns
    -------

    """
    import csv
    # sanity check
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be an instance of pd.DataFrame")
    if any(col not in df.columns for col in GTF_HEADER):
        raise ValueError("Not all expected columns (%s) are seen in the dataframe" % GTF_HEADER)

    # build attribute
    attr_cols = set(df.columns.values).difference(set(GTF_HEADER))

    def _ll(x):
        row = x.dropna()
        return '; '.join(f'{col} "{x[col]}"' for col in attr_cols if col in row.index)

    df["|_attr_|"] = df.apply(_ll, axis=1)
    sdf = df.loc[:, GTF_HEADER + ["|_attr_|", ]]
    if fill_empty:
        sdf = sdf.copy()  # avoid modifying the original df
        sdf.fillna({gtf_col: "." for gtf_col in GTF_HEADER}, inplace=True)
    sdf.to_csv(save_to, sep="\t", header=False, index=False, quoting=csv.QUOTE_NONE)
    df.drop(columns=["|_attr_|"], inplace=True)
