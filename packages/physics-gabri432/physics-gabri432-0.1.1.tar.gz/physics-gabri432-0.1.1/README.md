## physics-gabri432
![GitHub](https://img.shields.io/github/license/Gabri432/python-physics)

A library containing several physics formulas and constants for making various calculations.

## Project structure
- root
    - .gitignore
    - [license (MIT)](https://github.com/Gabri432/python-physics/blob/master/license)
    - pyproject.toml
    - README.md
    - setup.py
    - tests (folder)
    - src/physics (folder)
        - __init__.py
        - [classical.py](https://github.com/Gabri432/python-physics/blob/master/physics/classical.py)
        - [constants.py](https://github.com/Gabri432/python-physics/blob/master/physics/constants.py)
        - [mathem.py](https://github.com/Gabri432/python-physics/blob/master/physics/mathem.py)
        - [thermodynamics.py](https://github.com/Gabri432/python-physics/blob/master/physics/thermodynamics.py)
        - [electromagnetism.py](https://github.com/Gabri432/python-physics/blob/master/physics/electromagnetism.py)
        - [gravity.py](https://github.com/Gabri432/python-physics/blob/master/physics/gravity.py)
        - [fluids.py](https://github.com/Gabri432/python-physics/blob/master/physics/fluids.py)
        - [relativity.py](https://github.com/Gabri432/python-physics/blob/master/physics/relativity.py)

## Description
- `classical.py`, collection of formulas from Cinematics and Dynamics fields;
- `constants.py`, collection of constants from all fields;
- `electromagnetism.py`, collection of formulas from Electromagnetism field;
- `fluids.py`, collection of formulas from Fluids field;
- `gravity.py`, collection of formulas from Gravitation field;
- `mathem.py`, collection of utility math formulas;
- `relativity.py`, collection of formulas from Relativity field;
- `thermodynamics.py`, collection of formulas from Thermodynamics field;


## How to use it
```python
import physics
from physics import classical  #importing the classical module
print(classical.force(3,4))    #using a function from the classical module
```
### Result
```
>>> (12, 'N') // Respectevely, the result and the measurement unit
```
