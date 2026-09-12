# src/labor_costing/config.py
import os
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except Exception:
    # Fallback for environments where pydantic exposes these in the main package
    from pydantic import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    azure_sql_server: str
    azure_sql_database: str
    azure_sql_user: str
    azure_sql_password: str
    odbc_driver: str = "ODBC Driver 18 for SQL Server"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()