# config.py
import urllib.parse
import os

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    DB_USER = os.environ.get("THARUKA\tharu", "sa")
    DB_PASSWORD = os.environ.get("6116", "yourStrong(!)Password")
    DB_SERVER = os.environ.get("DB_SERVER", "localhost\\SQLEXPRESS")
    DB_NAME = os.environ.get("ARTISTSPORTALDB", "ArtistPortal")

    params = urllib.parse.quote_plus(
        # f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        # f"SERVER={DB_SERVER};"
        # f"DATABASE={DB_NAME};"
        # f"UID={DB_USER};"
        # f"PWD={DB_PASSWORD};"
        # "TrustServerCertificate=yes;"
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=THARUKA\MSSQL;"
        "DATABASE=ARTISTSPORTALDB;"
        "Trusted_Connection=Yes;"
        "TrustServerCertificate=Yes;"
    )

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
