[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/CSvoW5SF)
# Instructions

Complete [Activity 14: Python Packaging](https://classroom.github.com/a/V0uPkSQk) and have a Python package deployed on PyPi. The name of your package does not have to be "example-package" but it most end with your name. The package could do anything you like (not necessarily what is done in the tutorial). You need to push a file name **example.py** that illustrates a possible use of your package. 

# Grading

+3 I should be able to install your package using pip. 

+2 **example.py** uses the package and runts without any error. 

# pck_BrendanD

`pck_BrendanD` is a simple Python package that provides a friendly greeting.

## Installation

Install `pck_BrendanD` by running:

pip install pck_BrendanD

## Usage

To use the `greet` function from the `pck_BrendanD` package, follow these steps:

```python
from pck_BrendanD import mod

# Greet the world
print(mod.greet("World"))

# Greet a user by name
print(mod.greet("Brendan"))
