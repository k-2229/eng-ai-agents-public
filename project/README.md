# CS375 Lakehouse Project

This project implements a small DuckLake lakehouse using DuckDB and RustFS
(S3-compatible object storage).

## Data Sources

- COCO 2017 validation sample with COCO images and annotations.
- VisDrone-style video fragment metadata.

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

```bash
docker compose up -d
cat > README.md <<'EOF'
# CS375 Lakehouse Project

This project implements a small DuckLake lakehouse using DuckDB and RustFS
(S3-compatible object storage).

## Data Sources

- COCO 2017 validation sample with COCO images and annotations.
- VisDrone-style video fragment metadata.

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

```bash
docker compose up -d
git status
cat > README.md <<'EOF'
# CS375 Lakehouse Project

This project implements a small DuckLake lakehouse using DuckDB and RustFS
(S3-compatible object storage).

## Data Sources

- COCO 2017 validation sample with COCO images and annotations.
- VisDrone-style video fragment metadata.

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

```bash
docker compose up EOF
