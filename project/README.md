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

## Hugging Face Round-Trip

The curated Gold COCO category statistics table was published to the Hugging Face Hub:

https://huggingface.co/datasets/Kp2229/cs375-lakehouse-gold

The published dataset contains the curated `gold.category_statistics` table with 36 category-level records.

## Hugging Face Round-Trip

The curated Gold COCO category statistics table was published to the Hugging Face Hub:

https://huggingface.co/datasets/Kp2229/cs375-lakehouse-gold

The published dataset contains the `gold.category_statistics` table with 36 category-level records.
## Hugging Face

The curated Gold COCO category statistics table was published to:

https://huggingface.co/datasets/Kp2229/cs375-lakehouse-gold

The published dataset contains 36 rows.

## Final Verification

The project includes `versioning_demo.py`, which demonstrates snapshot history,
version-based time travel, timestamp-based time travel, the COCO crowded-scene
query, the VisDrone busy-fragment query, and Gold-layer row counts.

The final verification produced:

- 22 COCO raw images
- 143 COCO raw annotations
- 143 Silver COCO annotations
- 36 COCO Gold categories
- 21 COCO Gold image statistics
- 5 VisDrone raw fragments
- 5 VisDrone Silver fragments
- 4 VisDrone Gold busy fragments
- 1093+ DuckLake snapshots during development

RustFS was also verified to contain the physical lakehouse objects, and
`ducklake_list_files` was used to identify the Parquet file backing the Gold
category statistics table.

The final Gold dataset was published to:

https://huggingface.co/datasets/Kp2229/cs375-lakehouse-gold
