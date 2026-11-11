
from hypothesis import given, strategies as st
from processor import sanitize_meter_id, parse_consumption_readings, format_billing_summary


# Test 1: Fuzz sanitize_meter_id
@given(st.text() | st.none())
def test_sanitize_meter_id_no_crash(s):
    try:
        sanitize_meter_id(s)
    except Exception as e:
        assert False, f"sanitize_meter_id crashed with input {s!r}: {e}"


# Test 2: Fuzz parse_consumption_readings
@given(st.text() | st.none())
def test_parse_consumption_readings_safe(s):
    try:
        parse_consumption_readings(s)
    except Exception as e:
        assert False, f"parse_consumption_readings crashed with input {s!r}: {e}"


# Test 3: Fuzz format_billing_summary
@given(st.text() | st.none())
def test_format_billing_summary_safe(s):
    try:
        format_billing_summary(s)
    except Exception as e:
        assert False, f"format_billing_summary crashed with input {s!r}: {e}"
