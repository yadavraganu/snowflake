# Automatic Clustering
Snowflake stores a table’s data in micro-partitions. Among these micro-partitions, Snowflake organizes (i.e. clusters) data based  
on dimensions of the data. If a query filters, joins, or aggregates along those dimensions, fewer micro-partitions must be scanned  
to return results, which speeds up the query considerably.

You can set a cluster key to change the default organization of the micro-partitions so data is clustered around specific  
dimensions (i.e. columns). Choosing a cluster key improves the performance of queries that filter, join, or aggregate by  
the columns defined in the cluster key.

Snowflake enables Automatic Clustering to maintain the clustering of the table as soon as you define a cluster key. Once enabled,  
Automatic Clustering updates micro-partitions as new data is added to the table.

# Consideration for chosing clustering
- Biggest performance boost comes from a WHERE clause that filters on a column of the cluster key, but it can also improve the
  performance of other clauses and functions that act upon that same column (e.g. joins and aggregations).
- Ideal for range queries or queries with an inequality filter. Also improves an equality filter, but the Search Optimization
  Service is usually faster for point lookup queries.
- Available in Standard Edition of Snowflake.
- There can be only one cluster key.If different queries against a table act upon different columns, consider using the
  Search Optimization Service or a materialized view instead.
- The table contains a large number of micro-partitions. Typically, this means that the table contains multiple terabytes (TB) of data.
- The queries can take advantage of clustering. Typically, this means that one or both of the following are true:
  - The queries are selective. In other words, the queries need to read only a small percentage of rows
    (and thus usually a small percentage of micro-partitions) in the table.
  - The queries sort the data. (For example, the query contains an ORDER BY clause on the table.)
- A high percentage of the queries can benefit from the same clustering key(s). In other words, many/most queries select on,
  or sort on, the same few column(s).
- If your goal is primarily to reduce overall costs, then each clustered table should have a high ratio of queries to DML operations
  (INSERT/UPDATE/DELETE). This typically means that the table is queried frequently and updated infrequently.
- If you want to cluster a table that experiences a lot of DML, then consider grouping DML statements in large, infrequent batches.
