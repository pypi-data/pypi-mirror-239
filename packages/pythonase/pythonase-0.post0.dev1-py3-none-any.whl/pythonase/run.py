# coding=utf-8
from subprocess import Popen, PIPE


def run_command(cmd: str, raise_exception: bool = False):
    """Run command

    Parameters
    ----------
    cmd : str

    raise_exception : bool
        Raise an exception if the return code is not 0.

    Returns
    -------
    stdout : str

    stderr : str

    return_code : int

    """
    with Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE) as p:
        stdout, stderr = p.communicate()
        stderr = stderr.decode("utf-8")
        stdout = stdout.decode("utf-8")
    if raise_exception and p.returncode != 0:
        raise RuntimeError(stderr)
    return stdout, stderr, p.returncode
