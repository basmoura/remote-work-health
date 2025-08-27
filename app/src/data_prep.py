import re
from typing import Optional

import pandas as pd

# Regex compilado para capturar números seguidos de 'k' (80k, 120K, etc.)
K_RANGE_RE = re.compile(r"(\d+)\s*[kK]")
BURNOUT_MAP = {"Low": 1, "Medium": 2, "High": 3}


def load() -> pd.DataFrame:
    df = pd.read_csv("app/assets/data/remote_work_health.csv").pipe(_normalize_na)

    normalized_df = (
        df.loc[df["Industry"] == "Technology"]
        .copy()
        .assign(
            Avg_Salary=lambda d: d["Salary_Range"].map(
                extract_and_calculate_avg_salary
            ),
            Burnout_Level=lambda d: d["Burnout_Level"].map(BURNOUT_MAP).astype("Int64"),
        )
        .pipe(_expand_physical_health_issues)  # cria colunas dummies
        .drop(
            columns=["Physical_Health_Issues", "Salary_Range", "Survey_Date"],
            errors="ignore",
        )
    )

    normalized_df.columns = normalized_df.columns.str.lower()

    return normalized_df


def _normalize_na(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza NAs de colunas-chave para 'Unknown' ou mantém NA quando numérico.
    Ajuste as colunas conforme seu dataset.
    """
    out = df.copy()
    # Exemplo: só preencha texto com "Unknown"
    text_cols = [
        "Burnout_Level",
        "Mental_Health_Status",
        "Salary_Range",
        "Industry",
        "Physical_Health_Issues",
    ]
    for col in (c for c in text_cols if c in out.columns):
        out[col] = out[col].fillna("Unknown")
    return out


def _expand_physical_health_issues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza 'Physical_Health_Issues' (split por ';', strip, espaços->'_' em minúsculas)
    e cria colunas dummies binárias (0/1).
    """
    if "Physical_Health_Issues" not in df.columns:
        return df

    # Normalização de valores em uma série auxiliar
    norm = (
        df["Physical_Health_Issues"]
        .fillna("Unknown")
        .astype(str)
        .str.split(";")
        .apply(
            lambda items: [
                re.sub(r"\s+", "_", i.strip()).lower() for i in items if i.strip()
            ]
        )
        .apply(lambda items: ";".join(items) if items else "unknown")
    )

    dummies = norm.str.get_dummies(sep=";").astype("Int64")

    return df.join(dummies)


def extract_and_calculate_avg_salary(s: Optional[str]) -> Optional[int]:
    """
    Extrai a média da faixa salarial a partir de strings como '80k-120k'
    Retorna a média em valor inteiro (ex.: 100_000) ou None se não for possível.
    """
    if s is None or pd.isna(s) or not str(s).strip():
        return None

    text = str(s)

    # Captura todos os números seguidos de K (varias ocorrências)
    nums = [int(n) * 1000 for n in K_RANGE_RE.findall(text)]
    if len(nums) >= 2:
        return int(sum(nums[:2]) / 2)

    return None
