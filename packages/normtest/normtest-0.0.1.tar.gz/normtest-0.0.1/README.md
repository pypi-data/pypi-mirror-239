<img src="https://raw.githubusercontent.com/puzzle-in-a-mug/normtest/main/docs/_static/favicon-180x180.png" align="right" />

# normtest

<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"> <img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white"> <img src="https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white"> <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black"> <img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg">

This package has a series of tests used to check whether a set of sample data follows, at least approximately, the Normal distribution.

## Available tests (07/11/2023)

- Ryan-Joiner


## Install

```
pip install normtest
```

## Usage

To apply tests directly to the data, import the package as follows:

```python
import normtest as nm
```

And then apply the test by passing the dataset. For example, Ryan Joiner's test:

```python
import numpy as np
x_data = np.array([...])
result = nm.rj_test(x_data)
print(result)
```

However, if you want to extract more information about a test, you need to import the test directly:

```python
from normtest import ryan_joiner
```

This way, it is possible to generate graphs and obtain intermediate values from the test calculations. For example, to use the line up method:

```python
import matplotlib.pyplot as plt
fig = ryan_joiner.line_up(x_data, correct=False)
plt.savefig(...)
```



## License

- [BSD 3-Clause License](https://github.com/puzzle-in-a-mug/normtest/blob/main/LICENSE)
