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
        - [Body.py](https://github.com/Gabri432/python-physics/blob/master/src/physics/Body.py)
        - [classical.py](https://github.com/Gabri432/python-physics/blob/master/src/physics/classical.py)
        - [constants.py](https://github.com/Gabri432/python-physics/blob/master/src/physics/constants.py)
        - [mathem.py](https://github.com/Gabri432/python-physics/blob/master/physics/mathem.py)
        - [thermodynamics.py](https://github.com/Gabri432/python-physics/blob/master/src/physics/thermodynamics.py)
        - [electromagnetism.py](https://github.com/Gabri432/python-physics/blob/master/src/physics/electromagnetism.py)
        - [gravity.py](https://github.com/Gabri432/python-physics/blob/master/src/physics/gravity.py)
        - [fluids.py](https://github.com/Gabri432/python-physics/blob/master/src/physics/fluids.py)
        - [relativity.py](https://github.com/Gabri432/python-physics/blob/master/src/physics/relativity.py)

## Description
- `Body.py`, a class to ease the use of some formulas;
- `classical.py`, collection of formulas from Cinematics and Dynamics fields;
- `constants.py`, collection of constants from all fields;
- `electromagnetism.py`, collection of formulas from Electromagnetism field;
- `fluids.py`, collection of formulas from Fluids field;
- `gravity.py`, collection of formulas from Gravitation field;
- `mathem.py`, collection of utility math formulas;
- `relativity.py`, collection of formulas from Relativity field;
- `thermodynamics.py`, collection of formulas from Thermodynamics field;

## How to install it
```
pip install physics-gabri432
```


## How to use the library

### Use functions
```python
import physics
from physics import classical  #importing the classical module
print(classical.force(3,4))    #using a function from the classical module
```
### Result
```
>>> (12, 'N') // Respectevely, the result and the measurement unit
```

### Or create a custom object and use its methods
```python
from physics.Body import Body       #importing the Body class
earth = Body('Earth', 5.97e24, 0)   #Initializing a variable 'earth' with its name, mass and speed.
print(earth)                        #Showing the string representation of the class.
print(earth.grav_field(6.371e6))    #using a function from the classical module
```
### Result
```
>>> Name: Earth         // The string representation of a Body object
    Mass: 5.97e+24 kg
    Speed: 0 m/s.
>>> (9.810360234523877, 'm/s^2') // Respectevely, the result and the measurement unit
```
