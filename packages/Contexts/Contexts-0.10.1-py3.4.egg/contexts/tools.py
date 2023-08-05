import time as time_module
import pdb
import sys


def catch(func, *args, **kwargs):
    """
    Call the supplied function with the supplied arguments,
    catching and returning any exception that it throws.

    Arguments:
        func: the function to run.
        *args: positional arguments to pass into the function.
        **kwargs: keyword arguments to pass into the function.
    Returns:
        If the function throws an exception, return the exception.
        If the function does not throw an exception, return None.
    """
    try:
        func(*args, **kwargs)
    except Exception as e:
        return e


def time(func, *args, **kwargs):
    """
    Call the supplied function with the supplied arguments,
    and return the total execution time as a float in seconds.

    The precision of the returned value depends on the precision of
    `time.time()` on your platform.

    Arguments:
        func: the function to run.
        *args: positional arguments to pass into the function.
        **kwargs: keyword arguments to pass into the function.
    Returns:
        Execution time of the function as a float in seconds.
    """
    start_time = time_module.time()
    func(*args, **kwargs)
    end_time = time_module.time()
    return end_time - start_time


def set_trace():
    """Start a Pdb instance at the calling frame, with stdout routed to sys.__stdout__."""
    # https://github.com/nose-devs/nose/blob/master/nose/tools/nontrivial.py
    pdb.Pdb(stdout=sys.__stdout__).set_trace(sys._getframe().f_back)
