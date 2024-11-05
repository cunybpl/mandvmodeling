# MandVModeling

**_NOTE:_** This project is actively developed. Expect frequent updates and changes.

## Overview

MandVModeling is an open-source Python project for modeling and visualizing changepoint models. It provides tools for analyzing trends in time series data. Uses research-driven findings to make modifications and additions to [CUNYBPL's `changepointmodel` Github repository](https://github.com/cunybpl/changepointmodel).


## Table of Contents

1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Contributing](#contributing)
6. [License](#license)
7. [Acknowledgments](#acknowledgments)

## Differences from CUNYBPL's `changepointmodel`

- Use two different sets of bounds
    - `daily_bounds.py` calculates bounds using the outside air temperature data. These bounds should work for timeseries data with a daily granularity.
    - `default_bounds.py` calculates bounds using the outside air temperature data. The functions are carried over from the `cunybpl/changepointmodel` Github repo. These should work for any granularity and should therefore be used as the default bounds.
- Uses initial guesses
    - `scipy.optimize.curve_fit` allows for the use of initial guesses which should basically point the optimization "towards the right direction" and result in faster convergence. However, the initial guesses have to be within the defined bounds. With that being said, this package provides a `init_guesses.py` module, which works similarly to the `daily_bounds.py` and `default_bounds.py` files, which calculate initial guesses using the outside air temperature (defined as `X`) and energy consumption (defined as `y`). When in doubt, it is probably best to leave them defined as `None`. 
- `MandVDataModel`
    - This is a new dataclass which inherits from `CurvefitEstimatorDataModel`, located in `mandvmodeling.core.schemas`. While performing research related tasks, it was found that `EnergyChangepointEstimator` from the `cunybpl/changepointmodel` package required that the data was presorted by X before the data was fed into the `CurvefitEstimatorDataModel` instance. Therefore, this dataclass forcibly sorts the data by X.
- `MandVParameterModelFunction`
    - In `mandvmodeling.core.pmodels`, the `ParameterModelFunction` instance is inherited from the `ParameterModelFunction` in `cunybpl/changepointmodel`. This dataclass uses all of the parameters from the `ParameterModelFunction` in addition to a `initial_guesses` parameter which allows you to set initial guesses within the modeler.
- `MandVCurvefitEstimator`
    - This class inherits from `CurvefitEstimator` from `cunybpl/changepointmodel`. In `CurvefitEstimator`, the `fit` method does not allow you to use a `callable` as `p0`. This has been rectified in `MandVCurvefitEstimator`.
- `MandVEnergyChangepointEstimator`
    - This class inherits from `EnergychangepointEstimator` from `cunybpl/changepointmodel`. This uses a `MandVDataModel` instance, which contains `X` and `y`, which are used in model fitting and predicting. `EnergyChangepointEstimator` does not incorporate initial guesses into the class, while in `MandVEnergyChangepointEstimator`, the initial guesses from the `MandVParaneterModelFunction` instance are used.


## Project Structure

The project consists of several main components:

- `mandvmodeling/core`: Contains the machine learning modeling class `` and the data modeling class

## Installation

## Usage

## Features

- Supports various changepoint models (two-parameter, three-parameter, four-parameter, five-parameter)
- Generates boundary coordinates and changepoint coordinates
- Provides Plotly-based visualization tools
- Handles time series data analysis

## Future Work

- [] Import modified `bounds.py` and `init_guesses.py` file from `peterphung2043/changepointmodel` and perform unit tests for these two.
    - [] Make sure `bounds.py` and `init_guesses.py` natively support `cunybpl/changepointmodel`
    - [] Modify the README to reflect these differences
- [] Test the model coordinates parsers in `model_coordinates_parsers.py`
- [] Test the `PlotlyModelCoordinates`, `PlotlyRawDataCoordinates`, `PlotlyModelParameters`, `PlotlyRawDataParameters` dataclasses in the `plotly_parameters.py` file.
- [] Create test fixtures for the model coordinates parsers and the `PlotlyModelParameters` and `PlotlyRawDataParameters` dataclasses.
- [] Test every non-abstract-base-class class in `coordinates.py` and create relevant fixtures for these classes.
- [] Test and create fixtures for the `PlotlyParameterModelCoordinates` class in the `derive_model_coordinates.py` file.
- [] Test the `MandVModeling` class in the `estimator.py` file.
- [] Ensure that all of the `__init__.py` files in this repository have the relative imports
- [] Ensure that pydantic v2 is being used and is compatible with the entire package
- [] Ensure PEP 484 compliancy. Make sure everything has a specified type.
- [] Put up some badges on this readme to show relevant information about this package.
- [] [Use Github Actions to develop a Python workflow](https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the Python community for creating such powerful libraries like NumPy and Plotly.
- Inspiration drawn from various changepoint detection algorithms and visualizations.

---

This README provides an overview of the MandVModeling project structure, installation instructions, usage examples, features, contribution guidelines, license information, and acknowledgments. It serves as a starting point for users and contributors alike, providing essential information about the project's purpose, functionality, and how to engage with it.