USE lake;

CREATE OR REPLACE TABLE silver.visdrone_fragments AS
SELECT
    clip_uri,
    fragment_id,
    start_frame,
    end_frame,
    start_time,
    end_time,
    n_objects,
    classes
FROM raw.visdrone_fragments
WHERE end_frame > start_frame
  AND end_time > start_time
  AND n_objects >= 0;

ALTER TABLE silver.visdrone_fragments
ADD COLUMN IF NOT EXISTS project_demo VARCHAR DEFAULT 'cs375';
