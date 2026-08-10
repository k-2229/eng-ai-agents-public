# CS375 AI Lakehouse Project Report

## 1. DuckLake design and separation of metadata from data

This project uses DuckLake with DuckDB as the SQL query engine and RustFS as the S3-compatible object store. The main design principle is that metadata and data are stored separately. The DuckLake catalog is represented by the DuckDB metadata catalog, while the actual table data is stored as Parquet objects in RustFS.

This separation is useful because object storage is well suited for large immutable data files. The Parquet files can be stored cheaply and independently from the compute engine. DuckDB can query the data through DuckLake without requiring all of the data to be stored inside one database file. The catalog keeps track of schemas, tables, snapshots, and references to the underlying data files.

The project demonstrates this separation directly. The lakehouse catalog contains tables such as raw.coco_images, silver.coco_annotations_clean, and gold.category_statistics, while RustFS contains the underlying Parquet objects. For example, the Gold category statistics table is represented by a Parquet data file under the RustFS lakehouse/gold area.

The separation also makes concurrent access easier because the catalog provides transactional metadata while the data files remain immutable. Readers can use a consistent snapshot while new operations create newer snapshots. The tradeoff is that the catalog and object storage must remain consistent: metadata may reference files that must remain available in the object store.

## 2. Snapshots, time travel, and rollback

DuckLake represents changes using immutable snapshots. A change such as an insert, update, delete, or schema modification results in a new snapshot rather than overwriting the previous logical state.

This project contains a large snapshot history. The lakehouse verification showed more than 1,000 snapshots, including snapshots 1087 and 1088. Time travel was demonstrated using version numbers:

    SELECT COUNT(*)
    FROM lake.raw.coco_images
    AT (VERSION => 1087);

and:

    SELECT COUNT(*)
    FROM lake.raw.coco_images
    AT (VERSION => 1088);

Both historical states could be queried independently. Timestamp-based time travel was also demonstrated using the snapshot timestamp.

Snapshots make it possible to inspect an older state of a table even after later changes have occurred. A rollback can restore a previous logical state by moving the table back to an earlier version rather than modifying historical data files.

The project also demonstrated transactional rollback by inserting a deliberately bad row inside a transaction and issuing ROLLBACK. Before rollback, the table contained the bad row. After rollback, only the original row remained. This demonstrates the transactional principle used to protect a lakehouse from an unsuccessful change.

Keeping many snapshots has a storage and metadata cost. Old snapshots retain references to older data files, and those files cannot necessarily be removed until the corresponding historical versions are no longer needed. Snapshot retention therefore has to be managed in a production system.

## 3. Data quality without primary keys and constraints

DuckLake does not provide the traditional primary-key and constraint system used by many relational databases. Therefore, data quality must be enforced by the transformation pipeline.

The project handles this in the Silver layer. Raw COCO annotations are cleaned and typed before being used to build Silver tables. The Silver layer separates ingestion from curated data and provides a stable structure for downstream queries.

The Gold layer then aggregates the cleaned data. For example, gold.category_statistics calculates annotation counts, image counts, average area, and total area by category. The Gold tables therefore contain curated analytical data rather than raw records.

The project verified that COCO contains 143 raw annotations and 143 cleaned annotations, while the Gold category statistics contain 36 categories. These counts provide simple reproducibility and quality checks.

## 4. What happens during an INSERT

When data is inserted into a DuckLake table, several pieces of state are involved.

First, DuckDB executes the SQL operation against the DuckLake table. The data is written into Parquet data files. Those files are stored in the configured RustFS S3 bucket. The DuckLake catalog records the table metadata and the relationship between the logical table and its data files.

The catalog therefore contains metadata about the table, schema, snapshots, and files, while RustFS contains the actual Parquet bytes.

For example, the project verified a Gold category statistics data file with ducklake_list_files. The returned data-file URI pointed to the RustFS lakehouse/gold area. The local RustFS storage contained dozens of files, confirming that the actual data was separated from the SQL catalog.

This design means the SQL catalog does not need to contain the complete contents of every table. It manages the metadata and version history while object storage holds the bulk data.

## 5. Why use a SQL catalog

A SQL catalog makes metadata management transactional and queryable. Instead of relying only on individual metadata files next to Parquet files, DuckLake uses a SQL catalog that DuckDB can access directly.

This makes operations such as inspecting snapshots, schemas, tables, and file relationships convenient. The project used ducklake_snapshots to inspect the snapshot history and ducklake_list_files to inspect the data files associated with a table.

The tradeoff is that the catalog becomes an important coordination component. It must remain available and consistent with the object storage layer. File-only approaches can be simpler in some cases because there is less centralized metadata management, but a SQL catalog provides stronger transactional organization for the table state.

## 6. Images, video, and the VisDrone fragment index

The project does not place image pixels or complete video files directly into normal analytical DuckLake rows. Instead, the tables contain metadata and URIs that point to objects in RustFS.

For COCO, the raw image table contains image_id, image_uri, file_name, width, height, and split. The image URI points to the corresponding object in RustFS. The annotations table contains object metadata such as category, bounding-box information, and image URI.

This allows DuckDB to perform analytical queries without loading every image into memory.

The same principle is used for VisDrone. The fragment table contains clip URIs, fragment IDs, object counts, and object classes. The Gold table selects the busy fragments whose object counts exceed the project threshold.

The final query returned four busy fragments with object counts of 24, 27, 31, and 35. DuckDB can therefore identify the fragments that are most useful for a detection task using metadata before the media loader retrieves the actual video bytes.

## 7. Hugging Face round trip

The project also completes the lakehouse-to-Hugging-Face direction. The Gold COCO category statistics table was converted to a Hugging Face Dataset and published as:

https://huggingface.co/datasets/Kp2229/cs375-lakehouse-gold

The published dataset contains 36 rows and the columns category_name, annotation_count, image_count, average_area, and total_area.

The published dataset was loaded again using the Hugging Face datasets library, confirming that the round-trip dataset is readable.

## 8. Final verification

The final lakehouse verification produced:

- COCO raw images: 22
- COCO raw annotations: 143
- COCO cleaned annotations: 143
- COCO Silver image summaries: 21
- COCO Gold category statistics: 36
- COCO Gold image statistics: 21
- VisDrone raw fragments: 5
- VisDrone Silver fragments: 5
- VisDrone Gold busy fragments: 4

The project also verified that RustFS contains the physical lakehouse objects and that DuckLake can identify the corresponding Parquet data file for the Gold layer.

Overall, the project demonstrates the separation of compute, catalog, and storage; layered raw, Silver, and Gold transformations; immutable snapshots and time travel; multimodal metadata management; RustFS object storage; and a Hugging Face publishing workflow.
