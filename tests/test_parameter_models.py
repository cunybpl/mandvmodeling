from changepointmodel.core.pmodels import (
    TwoParameterModel,
    EnergyParameterModelCoefficients,
)
from changepointmodel.core.pmodels.coeffs_parser import TwoParameterCoefficientParser
from mandvmodeling.core.pmodels import MandVParameterModelFunction


def test_modelfunction():
    def f(X, y):
        return (X + y).squeeze()

    bound = (42,), (43,)
    parmeter_model = TwoParameterModel()
    parser = TwoParameterCoefficientParser()
    initial_guesses = (42, 43)

    model = MandVParameterModelFunction(
        "mymodel",
        f=f,
        bounds=bound,
        initital_guesses=initial_guesses,
        parameter_model=parmeter_model,
        coefficients_parser=parser,
    )
    assert model.name == "mymodel"
    assert model.f == f
    assert model.bounds == bound
    assert model.parameter_model == parmeter_model
    assert model.initial_guesses == initial_guesses

    # Since the default for `initial_guesses == None`, test this.
    model = MandVParameterModelFunction(
        "mymodel",
        f=f,
        bounds=bound,
        parameter_model=parmeter_model,
        coefficients_parser=parser,
    )

    assert model.initial_guesses is None

    assert model.parse_coeffs((42, 99)) == EnergyParameterModelCoefficients(
        42, [99], []
    )
