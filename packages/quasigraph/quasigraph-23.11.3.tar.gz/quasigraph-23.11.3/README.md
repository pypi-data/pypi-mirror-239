<p align="center">
<img src="https://raw.githubusercontent.com/leseixas/quasigraph/master/resources/logo.png" style="height: 120px"></p>

[![PyPI - License](https://img.shields.io/pypi/l/quasigraph?color=green&style=for-the-badge)](LICENSE.txt)    [![PyPI](https://img.shields.io/pypi/v/quasigraph?color=red&label=version&style=for-the-badge)](https://pypi.org/project/quasigraph/) 

**Quasigraph** is an open-source toolkit designed for generating chemical and geometric descriptors to be used in machine learning models.

## Installation

The easiest method to install quasigraph is by utilizing pip:
```bash
$ pip install quasigraph
```

## Getting started

```python
from ase.build import molecule
from quasigraph import QuasiGraph

# Initialize an Atoms object for water using ASE's molecule function
atoms = molecule('H2O')

# Instantiate a QuasiGraph object containing chemical and coordination numbers
qgr = QuasiGraph(atoms)

# Convert the QuasiGraph object into a pandas DataFrame
df = qgr.get_dataframe()

# Convert the QuasiGraph object into a vector
vector = qgr.get_vector()

```

# Descriptor

The descriptor can be separated into two parts, a chemical part and a geometric part.

## Chemical part

The chemical part of the descriptor employs the [Mendeleev library](https://github.com/lmmentel/mendeleev), incorporating atomic details like the group, period, covalent radius, and Pauling electronegativity for every element within the object.

For example, for water (H<sub>2</sub>O) we have the table:

|    |   group_id |   period |   covalent_radius |   en_pauling |
|---:|-----------:|---------:|------------------:|-------------:|
|  0 |         16 |        2 |                63 |         3.44 |
|  1 |          1 |        1 |                32 |         2.2  |
|  2 |          1 |        1 |                32 |         2.2  |

## Geometric part

The geometric part involves identifying all bonds and computing the coordination numbers for each atom, indicated as CN1. Additionally, the generalized coordination number (CN2) is determined by summing the coordination numbers of the neighboring ligands for each atom and normalizing this sum by the highest coordination number found in the molecule.

For example, for water (H<sub>2</sub>O) we have the the geometric data:

|   CN1 |   CN2 |
|------:|------:|
|     2 |     1 |
|     1 |     1 |
|     1 |     1 |

## License

This is an open source code under [MIT License](LICENSE.txt).

