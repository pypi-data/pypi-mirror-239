# coding=utf-8
import gzip
import os
import pandas as pd
from collections import defaultdict


VCF_HEADER = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL',
              'FILTER', 'INFO']


def parse(line):
    """Parse a single line from a VCF file and return a dict

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

    for i, col in enumerate(VCF_HEADER):
        result[col] = _get_value(fields[i])

    # INFO field consists of "key1=value;key2=value;...".
    # infos = [x for x in re.split(R_SEMICOLON, fields[8]) if x.strip()]
    infos = [x for x in fields[7].split(";") if x.strip()]

    for i, info in enumerate(infos, 1):
        # It should be key="value".
        try:
            key, value = info.split("=")
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

    Returns
    -------

    """
    if not value:
        return None

    # Strip double and single quotes.
    value = value.strip('"\'')

    # Return a list if the value has a comma.
    value = value.replace("[", "").replace("]", "")

    if ',' in value:
        pass
    # These values are equivalent to None.
    elif value in ['', '.', 'NA']:
        return None

    return value


def read_lines(filename):
    """Open an VCF file and generate a dict for each line.

    Parameters
    ----------
    filename : str
        path to the vcf file

    Returns
    -------
    yield
    """
    fn_open = gzip.open if filename.endswith('.gz') else open
    mode = "rt" if filename.endswith('.gz') else "r"

    with fn_open(filename, mode) as fh:
        for line in fh:
            if line.startswith('##'):
                continue
            elif line.startswith('#'):
                l = line[1:]
                global VCF_HEADER
                VCF_HEADER = l.strip().split()
            else:
                yield parse(line)


def parse_vcf(file_name, cache=1, cache_suffix="_pd_cache.csv"):
    """Parse VCF file

    Parameters
    ----------
    file_name : str
        path to plain VCF or gzipped VCF
    cache : int
        1 for generating cache
    cache_suffix : str
        suffix for cache file

    Returns
    -------
    vcf : pd.DataFrame
        parsed vcf file
    """
    assert os.path.exists(file_name), "Cannot access the file you provided."

    if cache and os.path.exists(file_name + cache_suffix):
        return pd.read_csv(file_name + cache_suffix, index_col=None)

    result = defaultdict(list)

    for i, line in enumerate(read_lines(file_name)):
        for key in line.keys():
            if key not in result:
                result[key] = [None] * i

        for key in result.keys():
            result[key].append(line.get(key, None))

    df = pd.DataFrame(result)
    if cache:
        df.to_csv(file_name + cache_suffix, index=False)
    return df
