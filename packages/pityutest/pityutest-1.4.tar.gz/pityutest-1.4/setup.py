from setuptools import setup, find_packages
import os
os.path.dirname(os.path.abspath('__file__'))
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pityutest",
    version="1.4",
    author="Pityu",
    author_email="pista1125@gmail.com",
    description="A description of your package",
    license="MIT",
    url="https://github.com/pista1125/pityutest",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages()
)
