---
layout: technical
title: Research Data Platform
category: Design Systems
difficulty: Advanced
description: Discussion around Back Of The Hand Calculations + Timing Considerations
---

## Problem Statement
Design a research dataset ingestion and retrieval platform for internal researchers.

Requirements:
- ingest large batch datasets and frequent incremental updates
- support metadata search by dataset name, tags, owner, date, and version
- datasets are used by downstream simulation jobs
- no silent corruption
- common restores should complete within 30 minutes
- cloud object storage is available
- cost matters
- eventual consistency for search is acceptable
- dataset reads are much heavier than writes

Give me:
- core components
- write path
- read path
- metadata/versioning strategy
- backup/recovery
- corruption detection
- scaling bottlenecks


## Components
Background Summary:
Ultimately we need to create a catalog of ingested datasets, where the datasets are set up at some candence to be ingested, along with some protocol. "Every Sunday at 8AM go pull 80GB of data from this SFTP with user/pass", or "Pull in this OLTP database and keep an operational copy sync into the data warehouse via CDC, backfilling only when necessary", along with many other styles of incremental (stream vs some cadence flat file) vs batch, push vs pull, etc.

Cost matters, so ideally we are only storing net new data, and we have the ability to go backwards in time for as-of features so data scientists / researchers can see data as it was at some time period such as "address for this company on Jan 01". Cloud storage is available for us to utilize, and so we can store underlying data to disk there while also supporting time travel. Dataset reads are much heavier than writes, so we want to be sure we store some information about frequency access to ensure we are storing data on cloud storage correctly, hot in hot storage, infrequent in cold, but with the same access patterns for researchers. 

Restores, backfills, etc should be completed within 30 minutes, so there need to be online restore pipelines for all major datasets. Corrupted data should be flagged for an engineer to review, and the previous version should be made available

Metadata service for querying to get underlying links to catalgos / object storage for researchers to analyze and pull from - this should be a REST API with a search layer that allows for pointed search, searching by tags, etc based on spec. 

We can assume:
- The metadata/catalog search layer is eventually consistent
- The dataset contents and version pointers should be strongly enough controlled that users do not read silently corrupted or half-published data
- Researchers primarily consume data through batch/analytic jobs, not low-latency REST row lookups
- A REST API exists for catalog metadata and dataset discovery, not for serving full dataset payloads directly

Components:
- Metadata Service is the backbone of most of this, it will help in data orchestration, versioning, etc
    - Simple PostgreSQL database should cover this. No need for K:V store or anything wild
    - Tables:
        - Dataset
            - Columns:
                - dataset_id: int
                - name: str
                - schema: struct<col_name, type>
                - owner: str
                - vendor: str
                - date_input: date
                - last_date_changed: date
                - tag_ref_id: int (reference to tags)
                - data_path_root: Path
                - is_daily: bool
                - is_incremental: bool
                - is_overwritten: bool
                - should_be_archived: bool
                - some other metadata can always be included here
        - Tags
            - Columns:
                - tag_ref_id: int
                - tag_id: int (index)
                - tag_key: str (semantic search, boolean, str length, etc)
                - tag_val: str (semantic search, boolean, str length, etc)
                - some other metadata
        - Pipelines
            - Columns:
                - pipeline_id: int
                - pipeline_name: str
                - pipeline_owner: str
                - conxn_info: struct<str, str>
                - schedule_id: int
                - ...
        - Schedule
            - Columns:
                - schedule_id: int
                - ...
        - PipelineRuns
            - Columns:
                - pipeline_id: int
                - start_date: datetime
                - end_date: datetime
                - success: bool
                - dataset_id: List[int] (pipeline can ingest multiple ID's)
                - ...
        - There can be other tables in here that help in versioning out datasets, I won't go into everything now as more will probably come up during discovery
    - The metadata service will be used by a large amount of other components
        - The orchestrator could check which pipeline(s) need to be ran for a dataset, potentially one or many need to be scheduled (or just have airflow do it) for a certain dataset
        - The actual underlying big data jobs (let's say Spark) will want to see the last pipeline runs, file paths data resided in, connection info, and other information for a pipeline
            - These jobs will also want to check what data they need to ingest and process. If backfilling is required with some new data processing logic for incremental, we can utilize lookups on PipelineRuns to figure out where to start from
    - I don't think it's useful for me to dive into all of the tables, columns, and exact standards as it's quite a broad solution, however the metadata service is the most critical piece of data storage in this as it allows us to have relatively "stateless" pipelines that simply utilize knowlege from the metadata service
- Jobs
    - After that there are multiple job types:
        - Batch: This is typical batch processing, you bring in, validate schema, etc...
        - Incremental batch: These might be daily files coming in, you need merge / upsert keys to ensure data is processed correctly
        - Incremental stream: Somehow we need timestamps to ensure if we do a major backfill event (batch) we can start incremental streaming from some offset
- Planes
    - The control plane should be backed by Kubernetes ensuring that our metadata service is up and running, any other core service is also running (highly available with replication and backups)
        - Our metadata service should have consistent replication to ensure that as data is processed we capture it, write to disk, and replicate it strongly consistently to potential backups. This should have strong consistency because writes here will be minimal, and we want to ensure all writes are stored. There are many more reads so we will have read replicas that should be 1:1 with the leader to ensure there aren't any deviations
        - Control plane spark runners can stand up highly available streaming jobs that have a highly available driver, with spot instance workers. This ensures cost is minimal, and spot instances can go down while a highly available driver can start retries on offsets from WAL CDC offsets
            - There is an entire section of doing this appropriately that we could spend time on, but I'm going to just say utilize the high availability spark driver K8's runners to ensure this is done correctly
        - Batch spark jobs can also have highly available driver nodes with spot workers, and these will go down eventually after completeing
        - Airflow orchestrator can also sit on Kubernetes, and airflow is responsible for Cron based scheduling of Spark jobs. It doesn't touch streaming jobs as those are always up 
            - Cloud storage events, Event Broker events, etc can continuously be consumed by other services which can start airflow
            - The most common scenario is utilizing something like EventBridge when a file lands in S3, and then having a small lambda start an ingestion job on Airflow to consume the file
            - This allows for event based ingestion of batch / incremental batch pipelines. Inside the application code is where these pipelines call the metadata service to ensure everything checks out, and will consume the files
    - Data plane
        - This is where our actual underlying Hive partitions, relational databases (metadata service backend), and cloud storage data sits. We can choose to ahve cloud providers manage databases for us, or we can manage ourselves in control plane, it depends on cost vs developer support time
- Appication Code
    - The actual application code itself is responsible for checking metadata service, comparing it to what's in ingestion / what it needs to go out and pull, and then ingesting data to a new S3 path and updating the pointers in metadata service
    - Old data should not be overwritten, it can be handled as historic data, and metadata service should have pointers updated to "latest data path" researchers can use for batch data
    - Incremental is tougher as you want to store versions of rows for as-of features, and technically batch jobs of full files can be turned into incremental batch jobs if there are primary keys and a set of attributes to hash
        - This involves a raw append only layer of new data rows with new attributes, and includes timestamps
        - This data should reside in S3 as open source Apache Delta data, and we shouldn't store any of this in the metadta service except for pointers to root directories, and "last seen" timestamps if it's incremental batch
        - This allows for SCD Type 2 calculations over incremental, batch, and incremental stremaing data

Alright, I am done writing. Going to summarize and call this done and see what I see

Covering the write path for a new full batch file:
- File lands in S3 `/root/dir_to_table/big_data_Jan08.gzip.txt` which triggers an S3 event notification to EventBridge / Kafka / some broker
    - Lambda (wakes up for event in event bridge topic), or some exhaust service polling Kafka would get the event trigger, and can simply just lookup in the metadata service which directory path routes to which dataset which routes to which pipeline_id needs to be triggered
    - Trigger airflow to run that job
- The job itself is started as a Spark batch job. It has absolutely no information passed to it by Airflow - it's stateless. It starts, checks the metadata table for dataset paths it cares about, and for now let's say it only checks `/root/dir_to_table/`
    - It will see the last file it saw was `big_data_Jan01.gzip.txt` on Jan01, and today is Jan08, so it's going to ingest the new file (the file names can be the same, this is just an examlpe to showcase)
    - It unzips the data into Spark Dataframe, checks the actual schema contents against schema provided in metadata service / schema registry, and validates the whole file or row-by-row if that's available
    - Once done, it can utilize the primary keys from metadata service and compare those against the current Hive data
        - `/root/hive/big_data_table/<dir_with_parquet_data>`
        - Let's say this data is fully partitioned by `hash(primary_keys)` with `rangeByPartition`
        - Let's also say the metadta service has a set of columns we care about, we can also hash those and compare `hash(cols)` to our stored data to see if any of it is new
        - Comparing the rows in `big_data_Jan08.gzip.txt` dataframe is just an inner join with this data, and the partitions help to ensure we don't do full scans of data. The lookup time is $O(log p) + O(scan P)$ where p is number of partitions for data skipping, and then P is the actual scanning of the full file to get the row
            - This gives us all of the rows we need to append to the raw layer as "new data" by comparing `hash(cols)`
            - Data that's been seen before can be discarded, we don't need it
        - Primary keys we haven't seen before are inserts, column updates are updates. Both row types are fully appended to the raw layer
        - If our data provider provides explicit deletes we can use them, otherwise the metadata service needs to let us know if we should consider no longer seen data as deletes. These are also appended to raw
    - We then do a merge upsert of all new raw data (or just the dataframes in Spark app code) to our Bronze layer / "physical data" in S3
    - At this point in time the metadata service doesn't need to update pointers - the same bronze table now has all up to date information, we also have history in our append only table.
- The raw append only table can be partiitoned by `month/week/day/`, and we can remove old parittions into S3 glacier (the data is in Bronze), or we can delete it if we no longer need it ever
- We now have a full record of every ID, it's attributes over time (SCD Type 2), and can backfill during any corruption or disaster recovery for at least as long as we have the data in raw before it goes to S3 lifecycle glacier. From here downstream tables and joins are done, and are much less worrisome because we can fix any errors without worrying about data redundancy or storage corruption - we have the raw dataset!
- If we do not want to store data this way in raw, we simply do a new materialization in `/root/give/big_data_table/Jan08` and update the metadata service to `<root>/Jan08`, while setting up anything beforehand to go to S3 glacier or be deleted!
