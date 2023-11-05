# ptspy

ptspy is a python package for visualization and creative coding. It's the python version of the popular [Pts.js](https://ptsjs.org) library. It's currently under active development and not ready for use.

# Install

```
conda create -n ptspy python=3.11 pip numpy
pip install flit
flit install --symlink
```

#### Creating requirements.txt

```
pipreqs .
```

OR

```
(venv) $ python -m pip install pip-tools
(venv) $ pip-compile pyproject.toml
```

## Develop

Install as local package:

```
pip install -e .
```

## Tests and benchmarks

Tests all

```
pytest
```

Skip or only Benchmarks

```
pytest --benchmark-only
pytest --benchmark-disable
```

Note that the files and folders must have named with "test" prefix or suffix in order for `pytest` to run them.

## Differences from Pts.js

- For simplicity, angles are in degress, not radian.

---

## pyproject template

Based on this template: https://github.com/microsoft/python-package-template
