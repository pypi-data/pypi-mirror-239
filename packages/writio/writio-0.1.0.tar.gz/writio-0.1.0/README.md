# writio

A file reading and writing library for `.csv`, `.yaml`, and `.json` files. You probably shouldn't use this.

![License](https://img.shields.io/github/license/fmatter/writio)
[![Tests](https://img.shields.io/github/actions/workflow/status/fmatter/writio/tests.yml?label=tests)](https://github.com/fmatter/writio/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/writio.svg)](https://pypi.org/project/writio)
![Versions](https://img.shields.io/pypi/pyversions/writio)

```python
from writio import load, dump

dic = load("dict.yaml")
dump(dic, "dict.json")
dic = load("dict.json")
df = load("table.csv")
```
