# v1.0.0

The changes in this release are as follows:

- Use two different sets of bounds
- Uses initial guesses
- New `MandVDataModel` dataclass
- New `MandVParameterModelFunction` class
- New `MandVCurvefitEstimator`class
- `MandVEnergyChangepointEstimator` class

Note that in this version, there are no tests that have been run on any of the modules.

## What's New

### Multiple Bounds Modules

`daily_bounds.py` calculates bounds using the outside air temperature data. These bounds should work for timeseries data with a daily granularity.

`default_bounds.py` calculates bounds using the outside air temperature data. The functions are carried over from the `cunybpl/changepointmodel` Github repo. These should work for any granularity and should therefore be used as the default bounds.

### Incorporates Initial Guess Callables

`scipy.optimize.curve_fit` allows for the use of initial guesses which should basically point the optimization "towards the right direction" and result in faster convergence. However, the initial guesses have to be within the defined bounds. With that being said, this package provides a `init_guesses.py` module, which works similarly to the `daily_bounds.py` and `default_bounds.py` files, which calculate initial guesses using the outside air temperature (defined as `X`) and energy consumption (defined as `y`). When in doubt, it is probably best to leave them defined as `None`. 

### New `MandVDataModel` Dataclass

This is a new dataclass which inherits from `CurvefitEstimatorDataModel`, located in `mandvmodeling.core.schemas`. While performing research related tasks, it was found that `EnergyChangepointEstimator` from the `cunybpl/changepointmodel` package required that the data was presorted by X before the data was fed into the `CurvefitEstimatorDataModel` instance. Therefore, this dataclass forcibly sorts the data by X.

### New `MandVParameterModelFunction` Class

In `mandvmodeling.core.pmodels`, the `ParameterModelFunction` instance is inherited from the `ParameterModelFunction` in `cunybpl/changepointmodel`. This dataclass uses all of the parameters from the `ParameterModelFunction` in addition to a `initial_guesses` parameter which allows you to set initial guesses within the modeler.

### New `MandVCurvefitEstimator` Class

This class inherits from `CurvefitEstimator` from `cunybpl/changepointmodel`. In `CurvefitEstimator`, the `fit` method does not allow you to use a `callable` as `p0`. This has been rectified in `MandVCurvefitEstimator`.

### New `MandVEnergyChangepointEstimator` Class

This class inherits from `EnergychangepointEstimator` from `cunybpl/changepointmodel`. This uses a `MandVDataModel` instance, which contains `X` and `y`, which are used in model fitting and predicting.

`EnergyChangepointEstimator` does not incorporate initial guesses into the class, while in `MandVEnergyChangepointEstimator`, the initial guesses from the `MandVParaneterModelFunction` instance are used.
