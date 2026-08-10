import duckdb

con = duckdb.connect("/workspace/metadata.duckdb")
con.execute(open("/workspace/sql/00_attach.sql").read())

print("=== SNAPSHOTS ===")
print(con.sql("SELECT * FROM ducklake_snapshots('lake')"))

print("\n=== CURRENT COCO IMAGE COUNT ===")
print(con.sql("SELECT COUNT(*) FROM lake.raw.coco_images"))

print("\n=== ADD A TEST ROW ===")
con.execute("""
INSERT INTO lake.raw.coco_images
VALUES (
  999999,
  's3://lakehouse/raw/coco/images/version-demo.jpg',
  'version-demo.jpg',
  100,
  100,
  'version-demo'
)
""")

print(con.sql("SELECT COUNT(*) FROM lake.raw.coco_images"))

print("\n=== SNAPSHOTS AFTER INSERT ===")
print(con.sql("SELECT * FROM ducklake_snapshots('lake')"))

con.close()
