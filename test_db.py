import pyodbc
print(pyodbc.drivers())

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=THARUKA\MSSQL;"
    "DATABASE=ARTISTSPORTALDB;"
    "Trusted_Connection=Yes;"
    "TrustServerCertificate=Yes;"
)


conn = pyodbc.connect(conn_str)
print("Connected!")