
import pytest
from water_utility_billing import (
    calculate_water_bill,
    check_meter_tampering
)


# 1. Invalid input: accounts must be a list
def test_invalid_accounts():
    with pytest.raises(ValueError):
        calculate_water_bill("invalid", 10.0)


# 2. Invalid input: base fee cannot be negative
def test_negative_base_fee():
    with pytest.raises(ValueError):
        calculate_water_bill([], -10.0)


# 3. Inactive account should be skipped
def test_inactive_account():
    accounts = [
        {
            "is_active": False,
            "usage_blocks": [50]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result == {
        "total_billed": 0.0,
        "status": "NO_ACTIVITY"
    }


# 4. Residential account: invalid, low and high usage
def test_residential_usage_branches():
    accounts = [
        {
            "is_active": True,
            "is_commercial": False,
            "has_leak_waiver": False,
            "usage_blocks": [0, -5, 30, 101, 50]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    # 10 + (30 * 1.5) + (101 * 4.5)
    # Residential high usage stops further processing.
    assert result["total_billed"] == 509.5
    assert result["status"] == "NORMAL"


# 5. Commercial account: low, medium and high usage
def test_commercial_usage_branches():
    accounts = [
        {
            "is_active": True,
            "is_commercial": True,
            "has_leak_waiver": False,
            "usage_blocks": [0, -5, 40, 75, 120]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    # 10 + (40 * 1.5) + (75 * 2.5) + (120 * 3.5)
    assert result["total_billed"] == 677.5
    assert result["status"] == "NORMAL"


# 6. Leak waiver: bill exceeds 200
def test_leak_waiver_deduction():
    accounts = [
        {
            "is_active": True,
            "is_commercial": True,
            "has_leak_waiver": True,
            "usage_blocks": [101]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    # 10 + (101 * 3.5) - 50 = 313.5
    assert result["total_billed"] == 313.5


# 7. Leak waiver: bill is below 200
def test_leak_waiver_without_deduction():
    accounts = [
        {
            "is_active": True,
            "has_leak_waiver": True,
            "usage_blocks": [10]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    # 10 + (10 * 1.5) = 25
    assert result["total_billed"] == 25.0


# 8. Leak waiver: bill is exactly 200
def test_leak_waiver_at_exact_threshold():
    accounts = [
        {
            "is_active": True,
            "is_commercial": True,
            "has_leak_waiver": True,
            "usage_blocks": [76]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    # 10 + (76 * 2.5) = 200
    # Waiver applies only when bill > 200.
    assert result["total_billed"] == 200.0


# 9. More than five flagged usage blocks
def test_excessive_flags():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [0, -1, 0, -2, 0, -3]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["status"] == "EXCESSIVE_FLAGS"


# 10. No activity when total bill is zero
def test_no_activity():
    result = calculate_water_bill([], 0.0)

    assert result == {
        "total_billed": 0.0,
        "status": "NO_ACTIVITY"
    }


# 11. Empty meter readings
def test_empty_meter_readings():
    assert check_meter_tampering([]) == "NO_DATA"


# 12. Two consecutive negative readings
def test_meter_tampering_detected():
    readings = [[-1, -2, 5]]

    assert check_meter_tampering(readings) == "TAMPER_SUSPECTED"


# 13. Negative readings separated by a non-negative reading
def test_meter_readings_clear():
    readings = [
        [-1, 0, -2],
        [5, 10, 15]
    ]

    assert check_meter_tampering(readings) == "CLEAR"
