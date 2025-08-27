# tests/test_load.py
import pandas as pd
import pytest
from data_prep import load


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Industry": ["Technology", "Finance", "Technology"],
            "Salary_Range": ["80k-120k", "100k+", None],
            "Burnout_Level": ["Low", "High", "Medium"],
            "Physical_Health_Issues": [
                "Back Pain; Eye Strain",
                "Leg Pain",
                "Head Ache",
            ],
            "Survey_Date": ["2024-01-01", "2024-02-01", "2024-03-01"],
            "Other": [1, 2, 3],
        }
    )


def test_load_pipeline(monkeypatch, sample_df):
    def fake_read_csv(path):
        assert path.endswith("app/assets/data/remote_work_health.csv")
        return sample_df

    monkeypatch.setattr(pd, "read_csv", fake_read_csv)

    out = load()

    # Apenas linhas de Technology
    assert set(out.index) == {0, 2}

    # Colunas dropadas
    for col in ["Physical_Health_Issues", "Salary_Range", "Survey_Date"]:
        assert col not in out.columns

    # Avg_Salary ok (linha 0 tem 80-120k; linha 2 era None -> None)
    assert out.loc[0, "avg_salary"] == 100_000
    assert pd.isna(out.loc[2, "avg_salary"])

    # Burnout mapeado para Int64
    assert out["burnout_level"].dtype.name == "Int64"
    assert out.loc[0, "burnout_level"] == 1  # Low -> 1
    assert out.loc[2, "burnout_level"] == 2  # Medium -> 2

    # Dummies criadas e coerentes
    expected_dummy_cols = {"back_pain", "eye_strain", "head_ache"}
    assert expected_dummy_cols.issubset(set(out.columns))

    # Linha 0: back_pain e eye_strain
    assert out.loc[0, "back_pain"] == 1
    assert out.loc[0, "eye_strain"] == 1
    # Linha 2: head_ache
    assert out.loc[2, "head_ache"] == 1
