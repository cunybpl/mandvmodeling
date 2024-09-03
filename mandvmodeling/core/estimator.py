from typing import Callable, Any
from changepointmodel.core import EnergyChangepointEstimator
from changepointmodel.core.estimator import check_not_fitted
from .schemas import EnergyOATDataModel

def check_data_model(method: Callable[..., Any]) -> Callable[...,Any]:
  """
  Helper decorator to raise a TypeError if the data_model argument is not of type EnergyOATDataModel. This
  ensures that the date is pre-sorted before being fit to the model.

  Args:
    method: Callable[..., Any]: The method to be decorated

  Returns:
    Callable[..., Any]: The decorated method
  """
  def wrapper(self, data_model):
    if not isinstance(data_model, EnergyOATDataModel):
      raise TypeError('data_model is of type {}. Must be of type EnergyOATDataModel'.format(type(data_model).__name__))
    return method(self, data_model)
  return wrapper

class MandVModeling(EnergyChangepointEstimator):
  """
  A child class which inherits from the EnergyChangepointEstimator parent class. You can access all of the properties
  and scores from the EnergyChangepointEstimator class from the changepointmodel library but this child class
  ensures that the data is sorted beforehand.
  """
  @check_data_model
  def fit(self, data_model: EnergyOATDataModel, **fit_params):
    """
    This is a wrapped around EnergyChangepointEstimator.fit that forces the data to be sorted by X. Use
    EnergyChangepointEstimator.fit if you don't need to force the data to be sorted by X.
    """
    self.data_model_ = data_model
    super().fit(X = self.data_model_.X, y = self.data_model_.y)
    return self

  @property
  @check_not_fitted
  def data_model(self) -> EnergyOATDataModel:
    """
    Returns the EnergyOATDataModel object used to fit the model.
    """
    return self.data_model_