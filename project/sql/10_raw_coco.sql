INSTALL ducklake;
LOAD ducklake;

USE lake;

CREATE TABLE IF NOT EXISTS raw.coco_images (
    image_id BIGINT,
    image_uri VARCHAR,
    file_name VARCHAR,
    width INTEGER,
    height INTEGER,
    split VARCHAR
);

CREATE TABLE IF NOT EXISTS raw.coco_annotations (
    annotation_id BIGINT,
    image_id BIGINT,
    category_id INTEGER,
    category_name VARCHAR,
    bbox_x DOUBLE,
    bbox_y DOUBLE,
    bbox_width DOUBLE,
    bbox_height DOUBLE,
    area DOUBLE,
    is_crowd BOOLEAN
);
