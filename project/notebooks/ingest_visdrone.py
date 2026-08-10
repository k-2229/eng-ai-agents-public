import duckdb
import boto3
import os
import json

DB = "/workspace/metadata.duckdb"

con = duckdb.connect(DB)
con.execute(open("/workspace/sql/00_attach.sql").read())

s3 = boto3.client(
    "s3",
    endpoint_url="http://rustfs:9000",
    aws_access_key_id="rustfsadmin",
    aws_secret_access_key="rustfsadmin",
    region_name="us-east-1",
)

# Create a small VisDrone-style fragment index.
# Video bytes live in object storage; the table stores only metadata/URIs.

con.execute("""
CREATE TABLE IF NOT EXISTS lake.raw.visdrone_fragments (
    clip_uri VARCHAR,
    fragment_id INTEGER,
    start_frame INTEGER,
    end_frame INTEGER,
    start_time DOUBLE,
    end_time DOUBLE,
    n_objects INTEGER,
    classes VARCHAR
)
""")

rows = [
    (
        "s3://lakehouse/raw/visdrone/videos/sample_clip_01.mp4",
        1, 0, 149, 0.0, 5.0, 24,
        "pedestrian,car,bus"
    ),
    (
        "s3://lakehouse/raw/visdrone/videos/sample_clip_01.mp4",
        2, 150, 299, 5.0, 10.0, 31,
        "pedestrian,car,truck"
    ),
    (
        "s3://lakehouse/raw/visdrone/videos/sample_clip_01.mp4",
        3, 300, 449, 10.0, 15.0, 18,
        "pedestrian,bicycle"
    ),
    (
        "s3://lakehouse/raw/visdrone/videos/sample_clip_02.mp4",
        1, 0, 149, 0.0, 5.0, 27,
        "car,bus,truck"
    ),
    (
        "s3://lakehouse/raw/visdrone/videos/sample_clip_02.mp4",
        2, 150, 299, 5.0, 10.0, 35,
        "pedestrian,car"
    ),
]

con.execute("DELETE FROM lake.raw.visdrone_fragments")
con.executemany(
    "INSERT INTO lake.raw.visdrone_fragments VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    rows
)

# Create a small object-store placeholder for the referenced video fragments.
for key in [
    "raw/visdrone/videos/sample_clip_01.mp4",
    "raw/visdrone/videos/sample_clip_02.mp4",
]:
    s3.put_object(
        Bucket="lakehouse",
        Key=key,
        Body=b"VisDrone sample video fragment placeholder"
    )

print("VisDrone raw fragments:", con.sql(
    "SELECT COUNT(*) FROM lake.raw.visdrone_fragments"
).fetchone()[0])

print(con.sql("""
SELECT clip_uri, fragment_id, start_frame, end_frame, n_objects
FROM lake.raw.visdrone_fragments
ORDER BY n_objects DESC
"""))

con.close()
