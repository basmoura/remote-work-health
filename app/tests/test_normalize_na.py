# tests/test_normalize_na.py
import pandas as pd
from data_prep import _normalize_na


def test_normalize_na_text_cols_only():
    df = pd.DataFrame(
        {
            "Burnout_Level": ["Low", None],
            "Physical_Health_Issues": [None, "Back Pain"],
            "Salary_Range": [None, "80k-120k"],
            "Industry": [None, "Technology"],
            "Some_Number": [1.5, None],
        }
    )
    out = _normalize_na(df)

    assert out.loc[1, "Burnout_Level"] == "Unknown"
    assert out.loc[0, "Physical_Health_Issues"] == "Unknown"
    assert out.loc[0, "Salary_Range"] == "Unknown"
    assert out.loc[0, "Industry"] == "Unknown"

    # Numérica não vira "Unknown"
    assert pd.isna(out.loc[1, "Some_Number"])
