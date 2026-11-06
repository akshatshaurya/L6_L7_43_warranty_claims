"""Property-based fuzz tests for the Warranty Claims application."""

import math
import string

from hypothesis import given, strategies as st

from warranty_claims import parse_claim, age_average, payable_charge


# Invalid inputs must be rejected deliberately with an application-level
# validation message, rather than leaking incidental Python exceptions.
def assert_safe_result(function, value, validator):
    try:
        result = function(value)
    except ValueError as exc:
        assert str(exc).startswith("Invalid "), (
            f"{function.__name__} leaked an unhandled ValueError: {exc!r}"
        )
    except Exception as exc:  # catches TypeError, AttributeError, ZeroDivisionError, etc.
        assert False, (
            f"{function.__name__} raised unexpected {type(exc).__name__} "
            f"for input {value!r}: {exc}"
        )
    else:
        validator(result)


def validate_claim_result(result):
    assert isinstance(result, tuple)
    assert len(result) == 2
    plan, months = result
    assert isinstance(plan, str) and plan.strip()
    assert isinstance(months, float)
    assert math.isfinite(months) and months >= 0


def validate_average_result(result):
    assert isinstance(result, int)
    assert result >= 0


def validate_charge_result(result):
    assert isinstance(result, float)
    assert math.isfinite(result)
    assert result >= 0


arbitrary_values = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans(),
)


@given(arbitrary_values)
def test_parse_claim_handles_arbitrary_inputs_safely(value):
    assert_safe_result(parse_claim, value, validate_claim_result)


@given(arbitrary_values)
def test_age_average_handles_arbitrary_inputs_safely(value):
    assert_safe_result(age_average, value, validate_average_result)


@given(arbitrary_values)
def test_payable_charge_handles_arbitrary_inputs_safely(value):
    assert_safe_result(payable_charge, value, validate_charge_result)


# Valid-input properties ensure that defensive checks preserve intended use.
@given(
    plan=st.text(alphabet=string.ascii_letters + " ", min_size=1, max_size=25)
        .filter(lambda value: bool(value.strip())),
    months=st.integers(min_value=0, max_value=1200),
)
def test_parse_claim_valid_values(plan, months):
    result = parse_claim(f"{plan}:{months}")
    assert result == (plan.strip().title(), float(months))


@given(ages=st.lists(st.integers(min_value=0, max_value=1200), min_size=1, max_size=30))
def test_age_average_valid_values(ages):
    csv_value = ",".join(str(age) for age in ages)
    assert age_average(csv_value) == sum(ages) // len(ages)


@given(
    charge=st.integers(min_value=0, max_value=1_000_000),
    discount=st.integers(min_value=0, max_value=1_000_000),
)
def test_payable_charge_valid_values(charge, discount):
    expected = max(float(charge) * 1.18 - float(discount), 0.0)
    assert math.isclose(payable_charge(f"{charge}|{discount}"), expected)


# Explicit edge cases make the intended validation contract easy to review.
def test_parse_claim_rejects_missing_separator():
    try:
        parse_claim("25")
    except ValueError as exc:
        assert str(exc).startswith("Invalid ")
    else:
        assert False, "Malformed claim should be rejected"


def test_age_average_rejects_empty_list():
    try:
        age_average("")
    except ValueError as exc:
        assert str(exc).startswith("Invalid ")
    else:
        assert False, "Empty age list should be rejected"


def test_payable_charge_rejects_missing_discount():
    try:
        payable_charge("1500|")
    except ValueError as exc:
        assert str(exc).startswith("Invalid ")
    else:
        assert False, "Missing discount should be rejected"
