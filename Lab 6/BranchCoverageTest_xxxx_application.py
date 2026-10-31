
import pytest
from water_utility_billing import (
    calculate_water_bill,
    check_meter_tampering
)


# 1. Invalid accounts type: first validation condition is True
def test_invalid_accounts_type():
    with pytest.raises(ValueError):
        calculate_water_bill("invalid", 10.0)


# 2. Negative base fee: second validation condition is True
def test_invalid_base_fee():
    with pytest.raises(ValueError):
        calculate_water_bill([], -10.0)


# 3. Valid empty accounts list
def test_empty_accounts():
    result = calculate_water_bill([], 10.0)

    assert result == {
        "total_billed": 0.0,
        "status": "NO_ACTIVITY"
    }


# 4. Inactive account: account is skipped
def test_inactive_account():
    accounts = [
        {
            "is_active": False,
            "usage_blocks": [50]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["status"] == "NO_ACTIVITY"


# 5. Missing is_active field defaults to False
def test_missing_active_field():
    result = calculate_water_bill([{}], 10.0)

    assert result["status"] == "NO_ACTIVITY"


# 6. Active account with empty usage blocks
def test_active_account_empty_usage():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": []
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["total_billed"] == 10.0
    assert result["status"] == "NORMAL"


# 7. Usage less than or equal to zero
def test_non_positive_usage():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [0, -10]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["status"] == "NORMAL"


# 8. Usage below or equal to 50
def test_low_usage_tier():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [50]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["total_billed"] == 85.0


# 9. Usage above 50 and equal to 100
def test_medium_usage_tier():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [51, 100]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    # 10 + (51 * 2.5) + (100 * 2.5)
    assert result["total_billed"] == 387.5


# 10. Residential usage above 100
def test_residential_high_usage():
    accounts = [
        {
            "is_active": True,
            "is_commercial": False,
            "usage_blocks": [101, 20]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    # Residential high usage stops further processing.
    assert result["total_billed"] == 464.5


# 11. Commercial usage above 100
def test_commercial_high_usage():
    accounts = [
        {
            "is_active": True,
            "is_commercial": True,
            "usage_blocks": [101]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["total_billed"] == 363.5


# 12. Missing commercial field defaults to False
def test_missing_commercial_field():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [101]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["total_billed"] == 464.5


# 13. Leak waiver is absent
def test_no_leak_waiver():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [10]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["total_billed"] == 25.0


# 14. Leak waiver is present and bill exceeds 200
def test_waiver_bill_above_200():
    accounts = [
        {
            "is_active": True,
            "is_commercial": True,
            "has_leak_waiver": True,
            "usage_blocks": [101]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["total_billed"] == 313.5


# 15. Leak waiver is present and bill equals 200
def test_waiver_bill_equal_to_200():
    accounts = [
        {
            "is_active": True,
            "is_commercial": True,
            "has_leak_waiver": True,
            "usage_blocks": [76]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["total_billed"] == 200.0


# 16. Leak waiver is present and bill is below 200
def test_waiver_bill_below_200():
    accounts = [
        {
            "is_active": True,
            "has_leak_waiver": True,
            "usage_blocks": [10]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["total_billed"] == 25.0


# 17. Flag count does not exceed five
def test_flags_within_limit():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [0, -1]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["status"] == "NORMAL"


# 18. Flag count exceeds five
def test_flags_exceed_limit():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [0, -1, 0, -2, 0, -3]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["status"] == "EXCESSIVE_FLAGS"


# 19. Total billed is zero
def test_zero_total_billed():
    result = calculate_water_bill([], 0.0)

    assert result["status"] == "NO_ACTIVITY"


# 20. Total billed is non-zero
def test_nonzero_total_billed():
    accounts = [
        {
            "is_active": True,
            "usage_blocks": [10]
        }
    ]

    result = calculate_water_bill(accounts, 10.0)

    assert result["status"] == "NORMAL"


# 21. Empty readings matrix
def test_empty_readings_matrix():
    assert check_meter_tampering([]) == "NO_DATA"


# 22. Meter exists but has no readings
def test_empty_individual_meter():
    assert check_meter_tampering([[]]) == "CLEAR"


# 23. One negative reading followed by a non-negative reading
def test_negative_counter_reset():
    readings = [[-1, 0, -2, 5]]

    assert check_meter_tampering(readings) == "CLEAR"


# 24. Two consecutive negative readings
def test_two_consecutive_negative_readings():
    readings = [[-1, -2]]

    assert check_meter_tampering(readings) == "TAMPER_SUSPECTED"


# 25. Multiple meters with no tampering
def test_multiple_meters_clear():
    readings = [
        [1, 2, 3],
        [-1, 0, 5],
        [10, 20, 30]
    ]

    assert check_meter_tampering(readings) == "CLEAR"
