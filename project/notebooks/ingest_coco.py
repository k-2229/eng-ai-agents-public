import json
import os
import io
import boto3
import requests
import duckdb

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BUCKET = "lakehouse"
S3_ENDPOINT = "http://rustfs:9000"
AWS_ACCESS_KEY = "rustfsadmin"
AWS_SECRET_KEY = "rustfsadmin"

# Small sample for the project
NUM_IMAGES = 20

# COCO 2017 validation images
IMAGE_BASE_URL = "http://images.cocodataset.org/val2017/"

# ---------------------------------------------------------
# RustFS / S3
# ---------------------------------------------------------

s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="us-east-1",
)

# Make sure bucket exists
buckets = [b["Name"] for b in s3.list_buckets()["Buckets"]]

if BUCKET not in buckets:
    s3.create_bucket(Bucket=BUCKET)
    print(f"Created bucket: {BUCKET}")
else:
    print(f"Bucket already exists: {BUCKET}")

# ---------------------------------------------------------
# Use the COCO JSON API package
# ---------------------------------------------------------

print("Downloading COCO validation annotations JSON...")

json_url = (
    "https://huggingface.co/datasets/"
    "pcuenq/coco2017-instances/resolve/main/"
    "instances_val2017.json"
)

response = requests.get(json_url, timeout=120)
response.raise_for_status()

coco = response.json()

images = coco["images"]
annotations = coco["annotations"]
categories = {
    c["id"]: c["name"]
    for c in coco["categories"]
}

# ---------------------------------------------------------
# Select a small deterministic sample
# ---------------------------------------------------------

images = sorted(images, key=lambda x: x["id"])[:NUM_IMAGES]

selected_ids = {img["id"] for img in images}

annotations = [
    ann
    for ann in annotations
    if ann["image_id"] in selected_ids
]

print("Selected images:", len(images))
print("Selected annotations:", len(annotations))

# ---------------------------------------------------------
# Connect to DuckLake
# ---------------------------------------------------------

con = duckdb.connect("/workspace/metadata.duckdb")

con.execute(open("/workspace/sql/00_attach.sql").read())

# Make ingestion reproducible: clear previous sample before reloading.
con.execute("DELETE FROM lake.raw.coco_images")
con.execute("DELETE FROM lake.raw.coco_annotations")

# ---------------------------------------------------------
# Upload images to RustFS
# ---------------------------------------------------------

print("Uploading images to RustFS...")

for i, image in enumerate(images, start=1):

    file_name = image["file_name"]

    image_url = IMAGE_BASE_URL + file_name

    print(
        f"[{i}/{len(images)}] downloading {file_name}"
    )

    image_response = requests.get(
        image_url,
        timeout=60,
    )

    image_response.raise_for_status()

    object_key = f"raw/coco/images/val2017/{file_name}"

    s3.put_object(
        Bucket=BUCKET,
        Key=object_key,
        Body=image_response.content,
        ContentType="image/jpeg",
    )

    image_uri = f"s3://{BUCKET}/{object_key}"

    con.execute(
        """
        INSERT INTO lake.raw.coco_images
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            image["id"],
            image_uri,
            file_name,
            image["width"],
            image["height"],
            "val2017",
            "initial_ingest",
        ],
    )

# ---------------------------------------------------------
# Insert annotations
# ---------------------------------------------------------

print("Inserting annotations...")

for ann in annotations:

    x, y, width, height = ann["bbox"]

    category_name = categories.get(
        ann["category_id"],
        "unknown",
    )

    con.execute(
        """
        INSERT INTO lake.raw.coco_annotations
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            ann["id"],
            ann["image_id"],
            ann["category_id"],
            category_name,
            x,
            y,
            width,
            height,
            ann["area"],
            bool(ann["iscrowd"]),
        ],
    )

print("COCO ingestion complete.")

# ---------------------------------------------------------
# Show verification
# ---------------------------------------------------------

print("\nImages:")
print(
    con.sql(
        """
        SELECT COUNT(*)
        FROM lake.raw.coco_images
        """
    ).fetchall()
)

print("\nAnnotations:")
print(
    con.sql(
        """
        SELECT COUNT(*)
        FROM lake.raw.coco_annotations
        """
    ).fetchall()
)

print("\nSample images:")
print(
    con.sql(
        """
        SELECT *
        FROM lake.raw.coco_images
        LIMIT 5
        """
    ).fetchall()
)

print("\nTop categories:")
print(
    con.sql(
        """
        SELECT
            category_name,
            COUNT(*) AS annotation_count
        FROM lake.raw.coco_annotations
        GROUP BY category_name
        ORDER BY annotation_count DESC
        LIMIT 10
        """
    ).fetchall()
)

con.close()
