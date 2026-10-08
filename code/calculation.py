import pandas as pd


# Cac cot chi phi hang thang
MONTHLY_COST_COLUMNS = [
    "compute_monthly_vnd",
    "storage_monthly_vnd",
    "network_monthly_vnd",
    "support_monthly_vnd",
    "operations_monthly_vnd",
]


def calculate_tco(data, months):
    """Tinh tong chi phi su dung dich vu trong so thang duoc chon."""
    monthly_cost = data[MONTHLY_COST_COLUMNS].sum(axis=1)
    tco = data["migration_one_time_vnd"] + monthly_cost * months
    return tco


def normalize_benefit(series):
    """Chuan hoa tieu chi cang cao cang tot, dung cho SLA."""
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series([100] * len(series), index=series.index)

    score = (series - min_value) / (max_value - min_value) * 100
    return score


def normalize_cost(series):
    """Chuan hoa tieu chi cang thap cang tot, dung cho TCO va Risk."""
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series([100] * len(series), index=series.index)

    score = (max_value - series) / (max_value - min_value) * 100
    return score


def rank_providers(data, months, sla_weight, tco_weight, risk_weight):
    """Tinh diem tong va xep hang cac nha cung cap Cloud."""
    result = data.copy()

    # Buoc 1: tinh TCO
    result["tco_vnd"] = calculate_tco(result, months)

    # Buoc 2: chuan hoa 3 tieu chi ve thang diem 0-100
    result["sla_score"] = normalize_benefit(result["sla_percent"])
    result["tco_score"] = normalize_cost(result["tco_vnd"])
    result["risk_score"] = normalize_cost(result["risk_level"])

    # Buoc 3: tinh diem tong theo trong so
    result["total_score"] = (
        result["sla_score"] * sla_weight / 100
        + result["tco_score"] * tco_weight / 100
        + result["risk_score"] * risk_weight / 100
    )

    # Buoc 4: lam tron va xep hang tu cao xuong thap
    result["total_score"] = result["total_score"].round(2)
    result = result.sort_values(by="total_score", ascending=False)
    result = result.reset_index(drop=True)

    result.index = result.index + 1
    result.index.name = "rank"

    return result
