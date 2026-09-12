# src/labor_costing/ingestion/api.py
import requests
import pandas as pd
from labor_costing.db import get_engine

NYC_SODA_URL = "https://data.cityofnewyork.us/resource/k397-673e.json"

def fetch_roster_data(agency: str = "DEPARTMENT OF TRANSPORTATION", year: int = 2024, limit: int = 50000) -> pd.DataFrame:
    params = {
        "$limit": limit,
        "$where": f"fiscal_year = {year} AND pay_basis = 'per Annum'",
        "agency_name": agency
    }
    response = requests.get(NYC_SODA_URL, params=params, timeout=30)
    response.raise_for_status()
    return pd.DataFrame(response.json())

def clean_roster(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = ["base_salary", "regular_gross_paid", "ot_hours", "total_ot_paid", "total_other_pay"]
    cleaned = pd.DataFrame({
        "fiscal_year": pd.to_numeric(df["fiscal_year"]),
        "agency_name": df["agency_name"],
        "title_description": df["title_description"],
        "agency_start_date": pd.to_datetime(df["agency_start_date"]).dt.date,
        "pay_basis": df["pay_basis"],
    })
    for col in numeric_cols:
        cleaned[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return cleaned

def load_roster_to_sql(df: pd.DataFrame):
    engine = get_engine()
    df.to_sql(name="raw_roster", schema="staging", con=engine, if_exists="append", index=False)