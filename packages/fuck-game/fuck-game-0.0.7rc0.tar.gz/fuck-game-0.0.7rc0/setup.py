from setuptools import setup, find_packages
import os 

os.environ['PYTHONPATH'] = 'src'
  
setup(
    name ='fuck-game',
    version ='0.0.7c',
    author ='4sushi',
    url ='https://github.com/4sushi/fuck',
    description ='Python game, made with curses',
    license ='MIT',
    packages = find_packages(),
    entry_points ={
        'console_scripts': [
            'fuck-game = main:main'
        ]
    },
    classifiers =(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires = [],
    zip_safe = False
)