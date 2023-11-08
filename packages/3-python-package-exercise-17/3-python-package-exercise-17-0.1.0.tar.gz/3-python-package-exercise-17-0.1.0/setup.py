# setup.py
from setuptools import setup, find_packages

setup(
    name='3-python-package-exercise-17',
    version='0.1.0',
    author='Chang Liu',
    author_email='cl5706@nyu.edu',
    packages=find_packages(),
    description='A simple Wordle-like game to play in the terminal.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        '': ['*.txt'],  #TODO: Add the word list file to the package data
    },
    entry_points={
        'console_scripts': [
            'wordle-game=python_package_exercise_17.simple_wordle:start_game',
        ],
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
