import os, sys, traceback

sys.path.insert(
    0, os.path.abspath("../..")
)  # Adds the parent directory to the system path
import dotapi
from dotapi import get_model_list

print(get_model_list())
print(get_model_list())
# print(anyllm.model_list)
