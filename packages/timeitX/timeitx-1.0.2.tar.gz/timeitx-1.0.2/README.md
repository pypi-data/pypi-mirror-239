# timeitX - Function Execution Time Logger

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/timeitX/1.0.1)](https://pypi.org/project/timeitX/) 
![GitHub issues](https://img.shields.io/github/issues/nitishsaik/timeitX)
[![PyPI version](https://badge.fury.io/py/timeitX.svg)](https://badge.fury.io/py/timeitX)
![GitHub](https://img.shields.io/github/license/nitishsaik/timeitX)
![GitHub](https://img.shields.io/github/issues/nitishsaik/timeitX)
![GitHub](https://img.shields.io/github/stars/nitishsaik/timeitX)
[![Downloads](https://pepy.tech/badge/timeitX/month)](https://pepy.tech/project/timeitX)

`timeitX` is a Python decorator that logs the execution time of functions, both for synchronous and asynchronous functions.

## Features

- Log the execution time of functions.
- Supports both synchronous and asynchronous functions.
- Customizable function names for logging.
- Precision down to milliseconds.
- Easy to integrate with your Python projects.

## Installation

You can install `timeitX` via pip:

```bash
pip install timeitX
```

## Usage

```python

from timeitX import timeitX

# Define your logger
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("timeitX")

@timeitX(name="My Function", logger=logger)
def my_function():
    # Your function code here

# For asynchronous functions
@timeitX(name="Async Function", logger=logger)
async def async_function():
    # Your async function code here

```
