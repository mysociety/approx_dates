from setuptools import setup, find_packages
from os.path import join, dirname

with open(join(dirname(__file__), 'README.rst')) as f:
    readme_text = f.read()

setup(
    name = "approx-dates",
    version = "0.0.1",
    packages = find_packages(),
    author = "Mark Longair",
    author_email = "mark@mysociety.org",
    description = "Classes for representing partial and approximate dates",
    long_description = readme_text,
    license = "MIT",
    keywords = "dates",
    install_requires = [
        'six >= 1.9.0',
    ]
)
