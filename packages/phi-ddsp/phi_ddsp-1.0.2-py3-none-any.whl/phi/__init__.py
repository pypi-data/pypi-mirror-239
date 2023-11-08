"""
phi

A conditional timbral model based off of DDSP

Author: Max Ardito 
"""

__version__ = "1.0.2"

# phi/__init__.py

# Import the functions you want to expose
from .preprocess import preprocess 
from .train import model_train

# Define __all__ to specify what's included with "from phi import *"
__all__ = ['preprocess', 'model_train']



