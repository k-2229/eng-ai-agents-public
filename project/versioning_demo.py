import duckdb

con = duckdb.connect("metadata.duckdb")
con.execute(open("sql/00_attach.sql").read())

print("=== SNAPSHOT HISTORY ===")
print(con.sql("""
SELECT snapshot_id, snapshot_time, commit_message
FROM ducklake_snapshots('lake')
ORDER BY snapshot_id DESC
LIMIT 10
"""))

print("\n=== TIME TRAVEL ===")
print(con.sql("""
SELECT COUNT(*) AS rows_at_1087
FROM lake.raw.coco_images AT (VERSION => 1087)
"""))

print(con.sql("""
SELECT COUNT(*) AS rows_at_1088
FROM lake.raw.coco_images AT (VERSION => 1088)
"""))

print("\n=== TIMESTAMP TIME TRAVEL ===")
print(con.sql("""
SELECT COUNT(*) AS rows_at_time
FROM lake.raw.coco_images
AT (TIMESTAMP => '2026-08-10 03:22:17+00')
"""))

print("\n=== COCO CROWDED SCENES ===")
print(con.sql("""
SELECT image_uri, COUNT(*) AS n_people
FROM lake.silver.coco_annotations_clean
WHERE category_name = 'person'
GROUP BY image_uri
HAVING COUNT(*) >= 5
ORDER BY n_people DESC
"""))

print("\n=== VISDRONE BUSY FRAGMENTS ===")
print(con.sql("""
SELECT clip_uri, fragment_id, n_objects, classes
FROM lake.gold.visdrone_busy_fragments
ORDER BY n_objects DESC
"""))

print("\n=== GOLD COUNTS ===")
print("COCO category statistics:",
      con.sql("SELECT COUNT(*) FROM lake.gold.category_statistics").fetchone()[0])
print("COCO image statistics:",
      con.sql("SELECT COUNT(*) FROM lake.gold.image_statistics").fetchone()[0])
print("VisDrone busy fragments:",
      con.sql("SELECT COUNT(*) FROM lake.gold.visdrone_busy_fragments").fetchone()[0])

con.close()
