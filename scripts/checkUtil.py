#!/usr/bin/env python

from contextlib import contextmanager
import os

# Context manager function for changing directory if necessary
@contextmanager
def working_directory(directory):
    owd = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(owd)
