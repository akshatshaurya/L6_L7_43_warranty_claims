"""Warranty claims input processing functions with defensive validation."""

import math


def _require_text(value, field_name):
    if not isinstance(value, str):
        raise ValueError(f"Invalid {field_name}: expected a string")
    return value.strip()


def parse_claim(text):
    """Parse a claim in 'plan:age_in_months' format.

    Returns:
        (normalized_plan_name, age_in_months)

    Raises:
        ValueError: if the input is malformed or contains an invalid age.
    """
    value = _require_text(text, "claim")
    if value.count(":") != 1:
        raise ValueError("Invalid claim: expected exactly one ':' separator")

    plan, months_text = value.split(":", 1)
    plan = plan.strip()
    months_text = months_text.strip()

    if not plan:
        raise ValueError("Invalid claim: plan must not be empty")
    if not months_text:
        raise ValueError("Invalid claim: age in months must not be empty")

    try:
        months = float(months_text)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Invalid claim: age in months must be numeric") from exc

    if not math.isfinite(months) or months < 0:
        raise ValueError("Invalid claim: age in months must be a finite non-negative number")

    return plan.title(), months


def age_average(ages_csv):
    """Return the floor of the average of comma-separated non-negative ages."""
    value = _require_text(ages_csv, "ages")
    if not value:
        raise ValueError("Invalid ages: at least one age is required")

    parts = value.split(",")
    ages = []

    for part in parts:
        part = part.strip()
        if not part:
            raise ValueError("Invalid ages: empty age value")
        try:
            age = int(part)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("Invalid ages: every age must be an integer") from exc
        if age < 0:
            raise ValueError("Invalid ages: ages must be non-negative")
        ages.append(age)

    return sum(ages) // len(ages)


def payable_charge(text):
    """Calculate max(charge * 1.18 - discount, 0) from 'charge|discount'."""
    value = _require_text(text, "charge")
    if value.count("|") != 1:
        raise ValueError("Invalid charge: expected exactly one '|' separator")

    charge_text, discount_text = value.split("|", 1)
    charge_text = charge_text.strip()
    discount_text = discount_text.strip()

    if not charge_text or not discount_text:
        raise ValueError("Invalid charge: charge and discount are both required")

    try:
        charge = float(charge_text)
        discount = float(discount_text)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Invalid charge: charge and discount must be numeric") from exc

    if not math.isfinite(charge) or not math.isfinite(discount):
        raise ValueError("Invalid charge: values must be finite")
    if charge < 0 or discount < 0:
        raise ValueError("Invalid charge: values must be non-negative")

    total = charge * 1.18 - discount
    if not math.isfinite(total):
        raise ValueError("Invalid charge: calculated total is outside the supported range")
    return max(total, 0.0)


def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    try:
        result = parse_claim(user_input)
        print("Plan and Age:", result)
    except ValueError as exc:
        print("Invalid claim:", exc)

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    try:
        result = age_average(user_input)
        print("Average Age:", result)
    except ValueError as exc:
        print("Invalid ages:", exc)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    try:
        result = payable_charge(user_input)
        print("Payable Charge:", result)
    except ValueError as exc:
        print("Invalid charge:", exc)


if __name__ == "__main__":
    main()
