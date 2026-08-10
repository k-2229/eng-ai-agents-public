CREATE OR REPLACE TABLE lake.gold.visdrone_busy_fragments AS
SELECT
    clip_uri,
    fragment_id,
    start_frame,
    end_frame,
    start_time,
    end_time,
    n_objects,
    classes
FROM lake.silver.visdrone_fragments
WHERE n_objects > 20
ORDER BY n_objects DESC;
