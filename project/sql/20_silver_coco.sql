USE lake;

CREATE OR REPLACE TABLE silver.coco_annotations_clean AS
SELECT
    a.annotation_id,
    a.image_id,
    i.file_name,
    i.image_uri,
    i.width,
    i.height,
    i.split,
    a.category_id,
    a.category_name,
    a.bbox_x,
    a.bbox_y,
    a.bbox_width,
    a.bbox_height,
    a.area,
    a.is_crowd
FROM raw.coco_annotations a
JOIN raw.coco_images i
    ON a.image_id = i.image_id
WHERE a.bbox_width > 0
  AND a.bbox_height > 0;

CREATE OR REPLACE TABLE silver.coco_image_summary AS
SELECT
    i.image_id,
    i.file_name,
    i.image_uri,
    i.width,
    i.height,
    i.split,
    COUNT(a.annotation_id) AS annotation_count,
    COUNT(DISTINCT a.category_id) AS category_count,
    COALESCE(SUM(a.area), 0) AS total_annotation_area
FROM raw.coco_images i
LEFT JOIN raw.coco_annotations a
    ON i.image_id = a.image_id
GROUP BY
    i.image_id,
    i.file_name,
    i.image_uri,
    i.width,
    i.height,
    i.split;
