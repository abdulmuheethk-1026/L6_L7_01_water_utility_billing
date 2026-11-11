from hypothesis import given, strategies as st
from processor import sanitize_meter_id, parse_consumption_readings, format_billing_summary

@given(st.text() | st.none())
def test_sanitize_meter_id_no_crash(s):
    #To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_parse_consumption_readings_safe(s):
    #To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_format_billing_summary_safe(s):
    #To-Do:Using try and except complete this function.
    pass