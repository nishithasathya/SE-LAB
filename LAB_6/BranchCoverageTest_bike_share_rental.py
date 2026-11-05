import pytest

from bike_share_rental import ride_cost, dock_status, can_unlock


# RIDE COST - BRANCH COVERAGE TESTS

@pytest.mark.parametrize(
    "bike_type, minutes, subscriber, peak, expected",
    [
        ("standard", 30, False, False, 20),
        ("electric", 60, False, False, 70),
        ("cargo", 30, False, False, 50),
        ("standard", 30, True, False, 0),
        ("standard", 60, True, False, 20),
        ("standard", 30, False, True, 35),
        ("cargo", 30, False, True, 50),
        ("standard", 181, False, False, 240),
    ],
)
def test_ride_cost_branches(bike_type, minutes, subscriber, peak, expected):
    assert ride_cost(bike_type, minutes, subscriber, peak) == expected


def test_unknown_bike_branch():
    with pytest.raises(ValueError):
        ride_cost("unknown", 30, False, False)


def test_invalid_duration_branch():
    with pytest.raises(ValueError):
        ride_cost("standard", -5, False, False)


# DOCK STATUS - BRANCH COVERAGE TESTS

@pytest.mark.parametrize(
    "bikes_docked, capacity, expected",
    [
        (0, 10, "empty"),
        (10, 10, "full"),
        (2, 10, "few bikes"),
        (8, 10, "few slots"),
        (5, 10, "available"),
    ],
)
def test_dock_status_branches(bikes_docked, capacity, expected):
    assert dock_status(bikes_docked, capacity) == expected


def test_invalid_capacity_branch():
    with pytest.raises(ValueError):
        dock_status(5, 0)


def test_negative_bikes_branch():
    with pytest.raises(ValueError):
        dock_status(-1, 10)


def test_excess_bikes_branch():
    with pytest.raises(ValueError):
        dock_status(11, 10)


# UNLOCK PERMISSION - BRANCH COVERAGE TESTS

@pytest.mark.parametrize(
    "balance, active_ride, age, expected",
    [
        (500, True, 25, False),
        (500, False, 15, False),
        (100, False, 17, True),
        (50, False, 18, True),
        (49, False, 18, False),
        (99, False, 17, False),
    ],
)
def test_unlock_branches(balance, active_ride, age, expected):
    assert can_unlock(balance, active_ride, age) == expected