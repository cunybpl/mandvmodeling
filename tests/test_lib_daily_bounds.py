import numpy as np
from mandvmodeling.core.calc.bounds import daily_bounds


def test_twop_daily_bounds():
    res = daily_bounds.twop()
    assert res == ((-np.inf, -np.inf), (np.inf, np.inf))


def test_threepc_daily_bounds():
    check_X = np.linspace(1.0, 10.0)
    res = daily_bounds.threepc(check_X)
    assert res == ((0, 0, 1.3673469387755102), (np.inf, np.inf, 9.63265306122449))


def test_threeph_daily_bounds():
    check_X = np.linspace(1.0, 10.0)
    res = daily_bounds.threeph(check_X)
    assert res == ((0, -np.inf, 1.3673469387755102), (np.inf, 0, 9.63265306122449))


def test_fourp_daily_bounds():
    check_X = np.linspace(1.0, 10.0)
    res = daily_bounds.fourp(check_X)
    assert res == (
        (0, -np.inf, 0, 1.3673469387755102),
        (np.inf, 0, np.inf, 9.63265306122449),
    )


def test_fivep_daily_bounds():
    check_X = np.linspace(1.0, 10.0)
    res = daily_bounds.fivep(check_X)
    assert res == (
        (0, -np.inf, 0, 1.3673469387755102, 1.9183673469387754),
        (np.inf, 0, np.inf, 9.081632653061225, 9.63265306122449),
    )
