import pytest

from bike_share_rental import (
    ride_cost,
    dock_status,
    can_unlock,
)


# -----------------------------------------
# RIDE COST - CODE COVERAGE TESTS
# -----------------------------------------

def test_standard_ride():
    assert ride_cost("standard", 45, False, False) == 40


def test_electric_ride():
    assert ride_cost("electric", 30, False, False) == 35


def test_cargo_ride():
    assert ride_cost("cargo", 60, False, False) == 100


def test_subscriber_free_ride():
    assert ride_cost("standard", 20, True, False) == 0


def test_subscriber_paid_ride():
    assert ride_cost("standard", 60, True, False) == 20


def test_peak_hour_surcharge():
    assert ride_cost("standard", 30, False, True) == 35


def test_cargo_peak_hour():
    assert ride_cost("cargo", 30, False, True) == 50


def test_long_ride_surcharge():
    assert ride_cost("standard", 181, False, False) == 240


def test_unknown_bike_type():
    with pytest.raises(ValueError):
        ride_cost("mountain", 30, False, False)


def test_invalid_ride_duration():
    with pytest.raises(ValueError):
        ride_cost("standard", 0, False, False)


# -----------------------------------------
# DOCK STATUS - CODE COVERAGE TESTS
# -----------------------------------------

def test_empty_dock():
    assert dock_status(0, 10) == "empty"


def test_full_dock():
    assert dock_status(10, 10) == "full"


def test_few_bikes():
    assert dock_status(2, 10) == "few bikes"


def test_few_slots():
    assert dock_status(8, 10) == "few slots"


def test_available_dock():
    assert dock_status(5, 10) == "available"


def test_invalid_capacity():
    with pytest.raises(ValueError):
        dock_status(5, 0)


def test_negative_bike_count():
    with pytest.raises(ValueError):
        dock_status(-1, 10)


def test_bike_count_exceeds_capacity():
    with pytest.raises(ValueError):
        dock_status(11, 10)


# -----------------------------------------
# UNLOCK PERMISSION - CODE COVERAGE TESTS
# -----------------------------------------

def test_active_ride_prevents_unlock():
    assert can_unlock(500, True, 25) is False


def test_underage_rider():
    assert can_unlock(500, False, 15) is False


def test_minor_with_sufficient_balance():
    assert can_unlock(100, False, 17) is True


def test_adult_with_sufficient_balance():
    assert can_unlock(50, False, 18) is True