import duckdb
import sys

con = duckdb.connect("/workspace/metadata.duckdb")

# Every SQL command needs the DuckLake catalog attached.
con.execute("""
INSTALL ducklake;
LOAD ducklake;

INSTALL httpfs;
LOAD httpfs;

CREATE OR REPLACE SECRET rustfs (
    TYPE s3,
    KEY_ID 'rustfsadmin',
    SECRET 'rustfsadmin',
    ENDPOINT 'rustfs:9000',
    URL_STYLE 'path',
    USE_SSL false
);

ATTACH 'ducklake:metadata.ducklake'
AS lake
(DATA_PATH 's3://lakehouse/');

USE lake;

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
""")

with open(sys.argv[1], "r") as f:
    sql = f.read()

# 00_attach only performs the same setup, so don't need to run it again.
if sys.argv[1].endswith("00_attach.sql"):
    print("DuckLake attached successfully.")
else:
    con.execute(sql)
    print("SQL completed successfully.")

con.close()
