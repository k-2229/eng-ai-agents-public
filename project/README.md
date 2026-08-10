# CS375 Lakehouse Project

This project implements a small DuckLake lakehouse using DuckDB and RustFS (S3-compatible object storage).

## Data Sources

- COCO 2017 validation sample with COCO images and annotations.
- VisDrone-style video fragment metadata.

## Lakehouse Layers

### Raw
- raw.coco_images
- raw.coco_annotations
- raw.visdrone_fragments

### Silver
- silver.coco_annotations_clean
- silver.coco_image_summary
- silver.visdrone_fragments

### Gold
- gold.category_statistics
- gold.image_statistics
- gold.visdrone_busy_fragments

## Rebuild

Start the services:

    docker compose up -d

Run the complete pipeline:

    docker compose exec lab ./rebuild.sh

## Verification

The project verifies:

- 20 COCO images
- 143 COCO annotations
- 143 cleaned COCO annotations
- 20 COCO image summaries
- 5 VisDrone fragments
- 5 cleaned VisDrone fragments
- 36 COCO category statistics
- 21 COCO image statistics
- 4 busy VisDrone fragments

## Versioning

versioning_demo.py demonstrates snapshot history, version-based time travel, timestamp-based time travel, COCO crowded-scene analysis, VisDrone busy-fragment analysis, and Gold-layer verification.

## Object Storage

RustFS stores the physical lakehouse objects. DuckLake file metadata is also used to verify the physical Parquet files.

## Hugging Face Round-Trip

The curated Gold COCO category statistics table was published to:

https://huggingface.co/datasets/Kp2229/cs375-lakehouse-gold

The published dataset contains 36 rows with category-level statistics.

## Project Structure

- docker-compose.yml - RustFS and DuckDB/Python environment
- run_sql.py - DuckLake SQL runner
- rebuild.sh - reproducible end-to-end rebuild
- notebooks/ - ingestion scripts
- sql/ - Raw, Silver, and Gold transformations
- versioning_demo.py - versioning and analytical verification
- REPORT.md - project design report
