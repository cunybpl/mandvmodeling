from changepointmodel.core.pmodels import (
    TwoParameterModel,
    EnergyParameterModelCoefficients,
)
from changepointmodel.core.pmodels.coeffs_parser import TwoParameterCoefficientParser
from mandvmodeling.core.pmodels import MandVParameterModelFunction
import pytest


def test_modelfunction():
    def f(X, y):
        return (X + y).squeeze()

    bound = (42,), (43,)
    parameter_model = TwoParameterModel()
    parser = TwoParameterCoefficientParser()
    initial_guesses = (42, 43)

    model = MandVParameterModelFunction(
        "mymodel",
        f=f,
        bounds=bound,
        initital_guesses=initial_guesses,
        parameter_model=parameter_model,
        coefficients_parser=parser,
    )
    assert model.name == "mymodel"
    assert model.f == f
    assert model.bounds == bound
    assert model.parameter_model == parameter_model
    assert model.initial_guesses == initial_guesses

    # Since the default for `initial_guesses == None`, test this.
    model = MandVParameterModelFunction(
        "mymodel",
        f=f,
        bounds=bound,
        parameter_model=parameter_model,
        coefficients_parser=parser,
    )

    assert model.initial_guesses is None

    assert model.parse_coeffs((42, 99)) == EnergyParameterModelCoefficients(
        42, [99], []
    )


def test_modelfunction_validator():
    def f(X, y):
        return (X + y).squeeze()

    bound = (42,), (43,)
    # Don't use instances like in `test_modelfunction`, just use
    # the classes themselves
    parameter_model = TwoParameterModel
    parser = TwoParameterCoefficientParser
    initial_guesses = (42, 43)

    model = MandVParameterModelFunction(
        "mymodel",
        f=f,
        bounds=bound,
        initital_guesses=initial_guesses,
        parameter_model=parameter_model,
        coefficients_parser=parser,
    )
    assert model.name == "mymodel"
    assert model.f == f
    assert model.bounds == bound
    assert model.parameter_model == parameter_model
    assert model.initial_guesses == initial_guesses

    # Use `parameter_model` class in the `coefficients_parser` param.
    with pytest.raises(TypeError):
        model = MandVParameterModelFunction(
            "mymodel",
            f=f,
            bounds=bound,
            initital_guesses=initial_guesses,
            parameter_model=parameter_model,
            coefficients_parser=parameter_model,
        )

    # Use `parser` class in the `parameter_model` param
    with pytest.raises(TypeError):
        model = MandVParameterModelFunction(
            "mymodel",
            f=f,
            bounds=bound,
            initital_guesses=initial_guesses,
            parameter_model=parser,
            coefficients_parser=parser,
        )

    with pytest.raises(TypeError):
        # Use `parser` class in the `f` param
        model = MandVParameterModelFunction(
            "mymodel",
            f=parser,
            bounds=bound,
            initital_guesses=initial_guesses,
            parameter_model=parser,
            coefficients_parser=parser,
        )
