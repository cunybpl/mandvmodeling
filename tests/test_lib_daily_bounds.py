import numpy as np
from mandvmodeling.core.calc.bounds import daily_bounds


def test_twop_daily_bounds():
    res = daily_bounds.twop()
    assert res == ((0, -np.inf), (np.inf, np.inf))


def test_threepc_daily_bounds():
    check_X = np.linspace(1.0, 10.0)
    res = daily_bounds.threepc(check_X)
    assert res == ((0, 0, 3.2040816326530615), (np.inf, np.inf, 7.795918367346939))


def test_threeph_daily_bounds():
    check_X = np.linspace(1.0, 10.0)
    res = daily_bounds.threeph(check_X)
    assert res == ((0, -np.inf, 3.2040816326530615), (np.inf, 0, 7.795918367346939))


def test_fourp_daily_bounds():
    check_X = np.linspace(1.0, 10.0)
    res = daily_bounds.fourp(check_X)
    assert res == (
        (0, -np.inf, -np.inf, 3.2040816326530615),
        (np.inf, np.inf, np.inf, 7.795918367346939),
    )


def test_fivep_daily_bounds():
    check_X = np.linspace(1.0, 10.0)
    res = daily_bounds.fivep(check_X)
    assert res == (
        (0, -np.inf, 0, 3.2040816326530615, 6.6938775510204085),
        (np.inf, 0, np.inf, 4.3061224489795915, 7.795918367346939),
    )
