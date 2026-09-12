# src/labor_costing/db.py
from sqlalchemy import create_engine
from labor_costing.config import settings

def get_engine():
    conn_str = (
        f"mssql+pyodbc://{settings.azure_sql_user}:{settings.azure_sql_password}@"
        f"{settings.azure_sql_server}/{settings.azure_sql_database}?"
        f"driver={settings.odbc_driver}&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
    )
    return create_engine(conn_str, fast_executemany=True)