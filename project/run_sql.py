import duckdb
import sys

con = duckdb.connect("/workspace/metadata.duckdb")

with open(sys.argv[1], "r") as f:
    sql = f.read()

con.execute(sql)

print("SQL completed successfully.")
