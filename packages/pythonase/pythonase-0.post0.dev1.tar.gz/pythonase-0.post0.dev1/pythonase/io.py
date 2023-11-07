# coding=utf-8
from pythonase.run import run_command
import pandas as pd


def to_csv_with_comments(df: pd.DataFrame, save_to: str, write_directory_version: bool = False,
                         additional_comment_lines: tuple = (), **to_csv_kwargs):
    """
    Export a DataFrame to csv files with comment lines

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be exported
    save_to : str
        Path
    write_directory_version : bool
        If True, the function tries to retrieve the corresponding Git commit ID from the
        working directory if the directory is part of a git repo
    additional_comment_lines : tuple
        Additional lines to be writen into the file. Items will be separate comments in the output file.
        Newline escape (\n) will be added automatically.
    to_csv_kwargs : kwargs
        kwargs to `pd.DataFrame.to_csv`
    Returns
    -------

    """
    with open(save_to, "w") as f:
        if write_directory_version:
            _, _, rc = run_command("git rev-parse --git-dir")
            if rc == 0:
                stdout, _, rc = run_command("git describe --tags --dirty --always")
                if rc == 0:
                    f.write(f"#Git commit: {stdout.strip()}\n")
            for line in additional_comment_lines:
                f.write(f"#{line}\n")
    write_mode = to_csv_kwargs.pop("mode", "a")
    df.to_csv(save_to, mode=write_mode, **to_csv_kwargs)
