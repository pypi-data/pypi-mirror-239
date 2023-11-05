from setuptools import setup, find_packages
import os

os.path.dirname(os.path.abspath('__file__'))


setup(
    name="pityutest",
    version="1.3",
    author="Pityu",
    author_email="pista1125@gmail.com",
    description="A description of your package",
    license="MIT",
    url="https://github.com/pista1125/pityutest",
    long_description="action",
    long_description_content_type='text/markdown',
    packages=find_packages()
)
