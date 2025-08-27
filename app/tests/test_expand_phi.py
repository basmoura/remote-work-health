# tests/test_expand_phi.py
import pandas as pd
from data_prep import _expand_physical_health_issues


def test_expand_phi_basic():
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "Physical_Health_Issues": [
                "Back Pain; Eye Strain",
                "eye strain ;   Head Ache",
                None,
            ],
        }
    )
    out = _expand_physical_health_issues(df)

    # Colunas dummy normalizadas
    expected_cols = {
        "back_pain",
        "eye_strain",
        "head_ache",
        "unknown",
    }
    assert expected_cols.issubset(set(out.columns))

    # Linhas corretas (Int64)
    assert out["back_pain"].dtype.name == "Int64"
    assert out.loc[0, "back_pain"] == 1
    assert out.loc[0, "eye_strain"] == 1
    assert out.loc[1, "eye_strain"] == 1
    assert out.loc[1, "head_ache"] == 1

    # Para None → "unknown" = 1
    assert out.loc[2, "unknown"] == 1

    # Mantém colunas originais
    assert "id" in out.columns
    assert "Physical_Health_Issues" in out.columns  # só é dropado no load()


def test_expand_phi_when_column_missing():
    df = pd.DataFrame({"id": [1, 2]})
    out = _expand_physical_health_issues(df)
    # Sem a coluna, não altera
    pd.testing.assert_frame_equal(out, df)
