from distutils.core import setup
import py2exe 
import math 


setup()

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': "main.pyw"}],
    zipfile = None,
)