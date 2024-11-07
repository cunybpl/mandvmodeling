"""
The tests for the `init_guesses.py` files. `np.linspace` allows us to create linearly spaced data when
specifying a minimum and maximum value. We then get arrays with values that incrementally increase
from the minimum to maximum value. This is important because this simulated pre-sorted data
which our M and V workflow needs.
"""

import numpy as np
from mandvmodeling.core.calc import init_guesses


def test_twop_init_guesses():
    check_X = np.linspace(27, 84)
    check_y = np.linspace(593, 1197)
    res = init_guesses.twop(check_X, check_y)
    assert res == (593, 10.596491228070175)


def test_threepc_init_guesses():
    check_X = np.linspace(27, 84)
    check_y = np.linspace(593, 1197)
    res = init_guesses.threepc(check_X, check_y)
    assert res == (593.0, 21.19298245614035, 55.5)
    # Check to see that the slope from init_guesses.threepc is calculated correctly
    assert res[1] == (
        (max(check_y) - min(check_y)) / (check_X[-1] - np.median(check_X))
    )
    # Check to see that the changepoint from init_guesses.threepc is calculated correctly
    assert res[2] == np.median(check_X)


def test_threeph_init_guesses():
    check_X = np.linspace(27, 84)
    check_y = np.linspace(593, 1197)
    res = init_guesses.threeph(check_X, check_y)
    assert res == (1197.0, -21.19298245614035, 55.5)
    # Check to see that the slope from init_guesses.threeph is calculated correctly
    assert res[1] == ((min(check_y) - max(check_y)) / (np.median(check_X) - check_X[0]))
    # Check to see that the changepoint from init_guesses.threeph is calculated correctly
    assert res[2] == np.median(check_X)


def test_fourp_init_guesses():
    # Simulate v-shaped data
    # Define the first range
    range_X_1 = np.linspace(27, 51)
    range_X_2 = np.linspace(52, 85)

    # Define the second range
    range_y_1 = np.linspace(1900, 1501)
    range_y_2 = np.linspace(1502, 1801)

    # Combine the ranges
    check_X = np.concatenate((range_X_1, range_X_2))
    check_y = np.concatenate((range_y_1, range_y_2))
    res = init_guesses.fourp(check_X, check_y)
    assert res == (1501.0, -16.625, 8.823529411764707, 51.0)
    # Check to see that m1 from init_guesses.fourp is calculated correctly
    assert res[1] == (
        (check_y[0] - min(check_y))
        / (check_X[0] - check_X[np.where(check_y == min(check_y))[0][0]])
    )
    # Check to see that m2 from init_guesses.fourp is calculated correctly
    assert res[2] == (
        (check_y[-1] - min(check_y))
        / (check_X[-1] - check_X[np.where(check_y == min(check_y))[0][0]])
    )
    # Check to see that cp from init_guesses.fourp is calculated correctly
    assert res[3] == check_X[np.where(check_y == min(check_y))[0][0]]


def test_fivep_init_guesses():
    # Simulate v-shaped data
    # Define the first range
    range_X_1 = np.linspace(27, 51)
    range_X_2 = np.linspace(52, 85)

    # Define the second range
    range_y_1 = np.linspace(1900, 1501)
    range_y_2 = np.linspace(1502, 1801)

    # Combine the ranges
    check_X = np.concatenate((range_X_1, range_X_2))
    check_y = np.concatenate((range_y_1, range_y_2))
    res = init_guesses.fivep(check_X, check_y)
    assert res == (1900.0, -16.285714285714285, 11.91044776119403, 37.0, 66.0)
    # Check to see that m1 from init_guesses.fivep is calculated correctly
    assert res[1] == ((min(check_y) - check_y[0]) / (np.median(check_X) - check_X[0]))
    # Check to see that m2 from init_guesses.fivep is calculated correctly
    assert res[2] == (
        (max(check_y) - min(check_y)) / (check_X[-1] - np.median(check_X))
    )
    # Check to see that cp1 from init_guesses.fivep is calculated correctly
    assert res[3] == np.median(check_X) - ((check_X[-1] - check_X[0]) * 0.25)
    # Check to see that cp2 from init_guesses.fivep is calculated correctly
    assert res[4] == np.median(check_X) + ((check_X[-1] - check_X[0]) * 0.25)
