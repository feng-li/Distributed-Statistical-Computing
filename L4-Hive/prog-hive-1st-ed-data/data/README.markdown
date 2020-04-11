# README for /data

This directory contains the few publically-available data sets used for the examples.

Note that some example HQL statements were tested with non-public data, which we can't make available. Let's discuss those first. Other statements were simply tested in with Hive but not used with any actual data. These examples are usually fairly obvious from the names chosen for the tables, columns, etc.

One of the cool features of Hive is that it's easy to create data in CSV, TSV, or other simple formats, put it in HDFS, and then start working with. We encourage you to do that when plaining with the examples for which we can't provide data.

## Non-public Data

The data sets discussed in the Case Studies are private, except where noted.

We discussed working with log data, such as the partitioning discussion in Chapter 4, "weblogs" in Chapter 9, and  "SerDes" discussed in Chapte 15. We used private data to develop these examples. However, it should be easy to obtain similar data and modify the schema appropriately to match the data or modify the data itself. For example, your peraonal computer probably has log files used internally. Your administrators can give you server logs. There are public Apache server logs available, too. [InfoChimps](http://infochimps.com/datasets) is one of many sources of public data.

We used arbitrary text files to play with the *WordCount* examples in Chapter 1. Any text files will do. Export your favorite *Word* documents to plain text and start playing.

## Public Data in This Directory Tree

Publically-accessible data obtained from other sources are noted in the table below. A few data sets were created ourselves.

| Name | Path | Source | Notes
| :--- | :--- | :----- | :----
| Stocks | `/data/stocks` | [InfoChimps](http://infochimps.com/datasets). Search for the datasets named `infochimps_dataset_4777_download_16185` and `infochimps_dataset_4778_download_16677`. | A subset of these datasets adapted for the book's format.
| Dividends | `/data/dividends` | Same [InfoChimps](http://infochimps.com/datasets) source. | Ditto
| Employees | `/data/employees` | Hand written by us. | A very short file demonstrating Hive's default text format.



