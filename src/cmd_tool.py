import os
import sys


def exit_enter(code=0):
    input('press enter to exit...')
    sys.exit(code)


def get_execution_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
