import os

DIR_SRC = os.path.dirname(os.path.abspath(__file__))
DIR_BASE = os.path.dirname(DIR_SRC)
DIR_OUTPUT = os.path.join(DIR_BASE, "output")

os.makedirs(DIR_OUTPUT, exist_ok=True)
