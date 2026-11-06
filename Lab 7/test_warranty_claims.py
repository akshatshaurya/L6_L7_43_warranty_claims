from hypothesis import given, strategies as st
from warranty_claims import parse_claim, age_average, payable_charge

@given(st.text() | st.none())
def test_parse_claim_no_crash(s):

@given(st.text() | st.none())
def test_age_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
