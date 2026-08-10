# CS375 Lakehouse Project

This project implements a small DuckLake lakehouse using DuckDB and RustFS
(S3-compatible object storage).

## Data Sources

- COCO 2017 validation sample: 20 images and their annotations.
- VisDrone-style video fragment metadata: 5 sample fragments.

## Lakehouse Layers

### Raw
- `raw.coco_images`
- `raw.coco_annotations`
- `raw.visdrone_fragments`

### Silver
- `silver.coco_annotations_clean`
- `silver.coco_image_summary`
- `silver.visdrone_fragments`

### Gold
- `gold.category_statistics`
- `gold.image_statistics`
- `gold.visdrone_busy_fragments`

## Rebuild

Start the services:

    docker compose up -d

Run the complete pipeline:

    docker compose exec lab ./rebuild.sh

The rebuild script attaches DuckLake, creates the required tables,
ingests the COCO and VisDrone data, and creates the Silver and Gold layers.

## Verification

The reproducible rebuild produces:

- 20 COCO images
- 143 COCO annotations
- 143 cleaned COCO annotations
- 20 COCO image summaries
- 5 VisDrone fragments
- 5 cleaned VisDrone fragments
- 36 COCO category statistics
- 20 COCO image statistics
- 4 busy VisDrone fragments

The VisDrone Gold layer identifies fragments containing more than
20 objects.

## Project Structure

- `docker-compose.yml` - RustFS and DuckDB/Python environment
- `run_sql.py` - DuckLake SQL runner
- `rebuild.sh` - reproducible end-to-end rebuild
- `notebooks/` - ingestion scripts
- `sql/` - Raw, Silver, and Gold transformations
