<p align="center">
<img src="https://raw.githubusercontent.com/delair-ai/python-delairstack/master/docs/images/SDK_Python.png" alt="logo" style="max-width:100%;">

<p align="center">
<a href="https://pypi.org/project/python-delairstack/" rel="nofollow"><img src="https://img.shields.io/pypi/v/python-delairstack.svg" alt="pypi version" style="max-width:100%;"></a>
<a href="https://pypi.org/project/python-delairstack/" rel="nofollow"><img src="https://img.shields.io/pypi/pyversions/python-delairstack.svg" alt="compatible python versions" style="max-width:100%;"></a>
</p>

> This SDK offers a high-level Python interface to [Delair.ai APIs](https://www.delair.ai).

## Installation

```python
pip install python-delairstack
```

**requires Python >= 3.4*

## Basic usage

```python
from delairstack import DelairStackSDK

sdk = DelairStackSDK(user="YOUR_EMAIL_ADDRESS",
                     password="YOUR_PASSWORD_ON_DELAIR.AI")

projects = sdk.projects.search(name='*')

for project in projects:
    print(project.name)

# My awesome project
```

<p>&nbsp;</p>

## 📕 Documentation

- [Reference documentation](https://python-delairstack.readthedocs.io/en/latest/index.html)
- [Getting started Jupyter notebook](https://nbviewer.jupyter.org/github/delair-ai/python-delairstack/blob/master/notebooks/getting_started.ipynb)