# v1.1.4

The changes in this release are as follows:

- In the `__init__` for `MandVEnergyChangepointEstimator`, `model` can be a `NoneType`
- In `MandVEnergyChangepointEstimator`, `data_model` is no longer retrievable.

## What's New

### `NoneType` for `model` in `MandVEnergyChangepointEstimator`

Before, the if-else statements would raise a `ValueError` if `model` was anything but an instance of type `MandVParameterModelFunction`. Now the if-else statement checks if `model` is `None`, if it's `None`, then the `MandVEnergyChangepointEstimator` instance still gets initialized and no `ValueError` is raised. This was done because `test_parameter_models.py` in `cunybpl/changepointmodel` has a `test_unfit_estimator_raises_notfittederror_on_property_access` unit test where `model` is `None`. This test was ported over to this package but failed because of the `ValueError`. But in this version, that test now passes.

## Removed retrievable `data_model` from `MandVEnergyChangepointEstimator`

In `MandVEnergyChangepointEstimator`, you can retrieve `X` and `y`, which are derived from the `MandVDataModel` instance used in the `fit` method. `MandVDataModel` contains in addition, the `sensor_reading_timestamps` parameter. Originally, you could retrieve the `data_model` instance from the `MandVEnergyChangepointEstimator`, but you could also in addition, retrieve the `X` and `y` from the same estimator too. Therefore, you could technically retrive the same array twice from the same estimator instance, by performing:

```
bounds = ((0, -np.inf), (np.inf, np.inf))
mymodel = MandVParameterModelFunction(
    name = "2P", 
    f = twop, 
    bounds = bounds, 
    parameter_model = TwoParameterModel(), 
    coefficients_parser = TwoParameterCoefficientParser()
)

X = np.linspace(1, 10, 10)
y = np.linspace(1, 10, 10)
sensor_reading_timestamps = [
    "2024-10-20",
    "2024-10-21",
    "2024-10-22",
    "2024-10-23",
    "2024-10-24",
    "2024-10-25",
    "2024-10-26",
    "2024-10-27",
    "2024-10-28",
    "2024-10-29",
]

data_model = MandVDataModel(
    X=X, y=y, sensor_reading_timestamps=sensor_reading_timestamps
)

est = MandVEnergyChangepointEstimator(mymodel)
est.fit(data_model)

#Retrieve `X` and `y` from the estimator
print(est.X)
print(est.y)

#Retrieve `X` and `y` from the `MandVDataModel` instance
#that is embedded inside the estimator itself 
print(est.data_model.X)
print(est.data_model.y)
```

The fact that you can retrieve X and y technically twice from the same object is redundant. Therefore, the `data_model` from the `MandVEnergyChangepointEstimator` instance is now privated. You can now directly retrieve the `sensor_reading_timestamps` array from the `data_model` instance. `sensor_reading_timestamps` is a new attribute that is not in `cunybpl/changepointmodel`'s `EnergyChangepointEstimator`.

# v1.1.3
 
 The changes in this release are as follows:

 - `_validate_param` validator created
    - Validates parameters in `MandVParameterModelFunction`

## What's New

### `_validate_param`

This new validator validates a parameter to ensure that it meets the required type criteria. This was created to type check the `f`, `parameter_model`, and `coefficients_parser` parameters in the `MandVParameterModelFunction` class. This ensures the following:
    - `f` must be a callable
    - `coefficients_parser` is a class which inherits from `cunybpl/changepointmodel.core.pmodels.base.ICoefficientParser`.
    - `parameter_model` is a class which inherits from `cunybpl/changepointmodel.core.pmodels.base.AbstractEnergyParameterModel`
This ensures that if new `parameter_model`s or new `coefficient_parser`s are created, they adhere to the abstract base classes defined in `cunybpl/changepointmodel.core.pmodels.base`. `f` has to be a callable because `scipy.optimize.curve_fit` requires it to be so.

# v1.1.2

The changes in this release are as follows:

- `Optional` erroneously imported from `pydantic` fixed
- Updated `MandVDataModel`

## What's New

### `Optional` Erroneously Imported from `pydantic` Fixed

In `mandvmodeling.core.schemas`, `Optional` was erronously imported from `pydantic` when it should have been imported from the `typing` module. This is now fixed

### Updated `MandVDataModel`

In the `validate_all` `pydantic.model_validator`, if the `order` was specified when creating an instance of `MandVDataModel`, this validator now checks that the length of `order` is the same as the length of `X`. Before, this was not checked, which meant that `order` could be any array of any length/size.

# v1.1.1

The changes in this release are as follows

- `MandVParameterModelFunction` now explicitly inherits from `typing.Generic`
- Fixed `__init__` in `MandVEnergyChangepointEstimator`
- `MandVDataModel` now has an `order` attribute

## What's New

### `MandVParameterModelFunction` Explicitly Inheriting from `typing.Generic`

What was found was that importing `MandVEnergyChangepointEstimator` resulted in the following `TypeError`:

```
TypeError: <class 'mandvmodeling.core.pmodels.parameter_model.MandVParameterModelFunction'> is not a generic class
```

`EnergyChangepointEstimator` in `cunybpl/changepointmodel` inherits from `typing.Generic`. Therefore, any `MandVParameterModelFunction` instance now explicity inherits from `typing.Generic` to circumvent the error.

### Fixed `__init__` in `MandVEnergyChangepointEstimator`

The definition for the `__init__` was:

```
def __init__(
    self,
    model=MandVParameterModelFunction[
            ParamaterModelCallableT, EnergyParameterModelT
        ]
)
```
The `=` sign should have been a `:` sign. This is now fixed.

### `MandVDataModel` `order` Attribute

This attribute was added in order for users to have access to the original ordering of the data before it is forcibly sorted by the `check_sorted``pydantic.model_validator`. This value is set by default as `None` and should be left that way as the `check_sorted``pydantic.model_validator` will set this value equal to a value of type `Ordering` (see `cunybpl/changepointmodel.core.nptypes`).

This attribute was also added so then the `MandVDataModel` ordering could be used natively to set the `original_ordering` attribute in an `MandVEnergyChangepointEstimator` instance (see `original_ordering.setter` in `cunybpl/changepointmodel`'s `EnergyChangepointEstimator`). 

If the order was unobtainable from `MandVDataModel`, then a `CurvefitEstimatorDataModel` instance would have had to have been created, from which the `sorted_X_y` method would be used.

# v1.0.1

The changes in this release are as follows:

- Entire package checked using [`ruff`](https://github.com/astral-sh/ruff)
- Entire package formatted using [`ruff`](https://github.com/astral-sh/ruff)

## What's New

Originally, [`black`](https://github.com/psf/black) was used for code formatting. But this was changed to `ruff`.

The entire package was checked using `ruff`. This:
    - Removed unnecessary imports
    - Fixed a problem in `test_schemas.py` where `test_MandVDataModel_forgot_timestamps` set a `MandVDataModelInstance` equal to `test`, but `test` was never used in the rest of the function.
The entire package was formatted using `ruff` for code readability.

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
