from distutils.core import setup
import py2exe
import os

setup(console=[os.path.join('src', 'asianet_login.py')])
