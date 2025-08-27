# tests/test_extract_salary.py
import pytest
from data_prep import extract_and_calculate_avg_salary


@pytest.mark.parametrize(
    "s,expected",
    [
        ("80k-120k", 100_000),
        ("No salary", None),
        ("", None),
        (None, None),
    ],
)
def test_extract_and_calculate_avg_salary(s, expected):
    assert extract_and_calculate_avg_salary(s) == expected
