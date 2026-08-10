#!/bin/bash
set -e

echo "=== Rebuilding DuckLake project ==="

python run_sql.py sql/00_attach.sql
python run_sql.py sql/10_raw_coco.sql

python notebooks/ingest_coco.py
python notebooks/ingest_visdrone.py

python run_sql.py sql/20_silver_coco.sql
python run_sql.py sql/21_silver_visdrone.sql

python run_sql.py sql/30_gold_coco.sql
python run_sql.py sql/31_gold_visdrone.sql

echo "=== Rebuild complete ==="
