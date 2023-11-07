# coding=utf-8
import time
import datetime
import sys


def message_with_time(msg: str, err: bool = False):
    """Print a message with a timestamp

    Parameters
    ----------
    msg : str
        Message
    err : bool
        Set as True if this is an error message

    Returns
    -------

    """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if err:
        sys.stderr.write("%s\t%s\n" % (st, msg))
    else:
        sys.stdout.write("%s\t%s\n" % (st, msg))
