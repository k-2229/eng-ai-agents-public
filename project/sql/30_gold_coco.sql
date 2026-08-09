USE lake;

CREATE OR REPLACE TABLE gold.category_statistics AS
SELECT
    category_name,
    COUNT(*) AS annotation_count,
    COUNT(DISTINCT image_id) AS image_count,
    ROUND(AVG(area), 2) AS average_area,
    ROUND(SUM(area), 2) AS total_area
FROM silver.coco_annotations_clean
GROUP BY category_name
ORDER BY annotation_count DESC;

CREATE OR REPLACE TABLE gold.image_statistics AS
SELECT
    image_id,
    file_name,
    width,
    height,
    annotation_count,
    category_count,
    ROUND(total_annotation_area, 2) AS total_annotation_area
FROM silver.coco_image_summary
ORDER BY annotation_count DESC;
