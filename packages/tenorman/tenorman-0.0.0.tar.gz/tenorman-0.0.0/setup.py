from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tenorman',
    version=os.environ.get('TENORMAN_VERSION', '0.0.0'),
    packages=['actions'],
    install_requires=[
        'pandas==2.1.1'
        ,'numpy==1.26.0'
        ,'matplotlib==3.8.0'
        ,'scipy==1.11.2'
        ,'cvxpy==1.3.2'
        ,'O365==2.0.28'
        ,'ccy==1.3.1'],
    python_requires='>=3.9',
    description='Tenorman is a Python package for tenor management.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)