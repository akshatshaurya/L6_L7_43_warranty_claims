
import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# OUT OF WARRANTY CHARGE TESTS

def test_unknown_plan():
    with pytest.raises(ValueError):
        out_of_warranty_charge("invalid", 30, "defect", False)


def test_invalid_age():
    with pytest.raises(ValueError):
        out_of_warranty_charge("standard", -1, "defect", False)


def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_registered_standard_plan():
    assert out_of_warranty_charge("standard", 25, "defect", True) == 0


def test_premium_registration_no_extra_coverage():
    assert out_of_warranty_charge("premium", 40, "defect", True) == 400


def test_normal_claim():
    assert out_of_warranty_charge("standard", 25, "defect", False) == 100


def test_accidental_claim():
    assert out_of_warranty_charge("standard", 25, "accidental", False) == 200


def test_excess_above_12_months():
    assert out_of_warranty_charge("standard", 37, "defect", False) == 1950


def test_accidental_claim_above_12_months():
    assert out_of_warranty_charge("standard", 37, "accidental", False) == 3575


# CLAIM ALLOWED TESTS

def test_recall_claim_allowed():
    assert claim_allowed(10, 5, True) is True


def test_recall_claim_limit_exceeded():
    assert claim_allowed(10, 6, True) is False


def test_claim_within_30_days():
    assert claim_allowed(20, 1, False) is False


def test_normal_claim_allowed():
    assert claim_allowed(60, 2, False) is True


def test_normal_claim_limit_exceeded():
    assert claim_allowed(60, 3, False) is False


# SLA STATUS TESTS

def test_hardware_on_track():
    assert sla_status(48, True, False) == "on_track"


def test_hardware_at_risk():
    assert sla_status(36, True, False) == "at_risk"


def test_hardware_critical():
    assert sla_status(35, True, False) == "critical"


def test_software_on_track():
    assert sla_status(24, False, False) == "on_track"


def test_software_at_risk():
    assert sla_status(12, False, False) == "at_risk"


def test_software_critical():
    assert sla_status(11, False, False) == "critical"


def test_priority_hardware():
    assert sla_status(72, True, True) == "on_track"


def test_priority_software():
    assert sla_status(48, False, True) == "on_track"
