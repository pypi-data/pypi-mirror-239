from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Simple library for creating multilayer Neural Networks '
LONG_DESCRIPTION = 'Library for Creating multiplayer Neural Networks less then 10 lines of code to train on MNIST'

# Setting up
setup(
    name="SwiftNet",
    version=VERSION,
    author="Michael Noel",
    author_email="mjn2024@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=['SwiftNet'],
    install_requires=['numpy', 'python-mnist', 'flask'],
    keywords=['python', 'AI', 'Neural Networks', 'Machine Learning', 'Simple', 'mnist'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)