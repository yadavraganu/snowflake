Copy Options

###################################################################################################################################
ON_ERROR = CONTINUE | SKIP_FILE | SKIP_FILE_<num> | SKIP_FILE_<num>% | ABORT_STATEMENT

CONTINUE--Continue to load the file if errors are found. The COPY statement returns an error message for a maximum of one error found per data file.

SKIP_FILE--Skip a file when an error is found.Note that the SKIP_FILE action buffers an entire file whether errors are found or not. For this reason, SKIP_FILE is slower than either CONTINUE or ABORT_STATEMENT. Skipping large files due to a small number of errors could result in delays and wasted credits. When loading large numbers of records from files that have no logical delineation (e.g. the files were generated automatically at rough intervals), consider specifying CONTINUE instead.

SKIP_FILE_<num>--Skip a file when the number of error rows found in the file is equal to or exceeds the specified number.

SKIP_FILE_<num>%--Skip a file when the percentage of error rows found in the file exceeds the specified percentage.

ABORT_STATEMENT--Abort the load operation if any error is found in a data file.
Note that the load operation is not aborted if the data file cannot be found (e.g. because it does not exist or cannot be accessed), except when data files explicitly specified in the FILES parameter cannot be found.

All ON_ERROR values work as expected when loading structured data files (CSV, TSV, etc.) with either parsing or transformation errors.

However, semi-structured data files (JSON, Avro, ORC, Parquet, or XML) do not support the same behavior semantics as structured data files for the following ON_ERROR values: CONTINUE, SKIP_FILE_num, or SKIP_FILE_num% due to the design of those format types.

Parquet and ORC data only. When ON_ERROR is set to CONTINUE, SKIP_FILE_num, or SKIP_FILE_num%, any parsing error results in the data file being skipped. Any conversion or transformation errors follow the default behavior of ABORT_STATEMENT (COPY INTO <table> statements) or SKIP_FILE (Snowpipe) regardless of the selected option value.

JSON, XML, and Avro data only. When ON_ERROR is set to CONTINUE, SKIP_FILE_num, or SKIP_FILE_num%, all records up to the record that contains the parsing error are loaded, but the remainder of the records in the data file are skipped. Any conversion or transformation errors follow the default behavior of COPY (ABORT_STATEMENT) or Snowpipe (SKIP_FILE) regardless of selected option value.

Default
Bulk loading using COPY--ABORT_STATEMENT
Snowpipe--SKIP_FILE

###################################################################################################################################

SIZE_LIMIT = <num>

Number (> 0) that specifies the maximum size (in bytes) of data to be loaded for a given COPY statement. When the threshold is exceeded, the COPY operation discontinues loading files. This option is commonly used to load a common group of files using multiple COPY statements. For each statement, the data load continues until the specified SIZE_LIMIT is exceeded, before moving on to the next statement.

For example, suppose a set of files in a stage path were each 10 MB in size. If multiple COPY statements set SIZE_LIMIT to 25000000 (25 MB), each would load 3 files. That is, each COPY operation would discontinue after the SIZE_LIMIT threshold was exceeded.

Note that at least one file is loaded regardless of the value specified for SIZE_LIMIT unless there is no file to be loaded.

###################################################################################################################################

PURGE = TRUE | FALSE

Boolean that specifies whether to remove the data files from the stage automatically after the data is loaded successfully.

If this option is set to TRUE, note that a best effort is made to remove successfully loaded data files. If the purge operation fails for any reason, no error is returned currently. We recommend that you list staged files periodically (using LIST) and manually remove successfully loaded files, if any exist.

###################################################################################################################################

RETURN_FAILED_ONLY = TRUE | FALSE

Boolean that specifies whether to return only files that have failed to load in the statement result.

###################################################################################################################################

MATCH_BY_COLUMN_NAME = CASE_SENSITIVE | CASE_INSENSITIVE | NONE
String that specifies whether to load semi-structured data into columns in the target table that match corresponding columns represented in the data.
MATCH_BY_COLUMN_NAME cannot be used with the VALIDATION_MODE parameter in a COPY statement to validate the staged data rather than load it into the target table
Supported Files
JSON
Avro
ORC
Parquet
###################################################################################################################################
ENFORCE_LENGTH = TRUE | FALSE
If TRUE, the COPY statement produces an error if a loaded string exceeds the target column length.
If FALSE, strings are automatically truncated to the target column length.
###################################################################################################################################
TRUNCATECOLUMNS = TRUE | FALSE
If TRUE, strings are automatically truncated to the target column length.
If FALSE, the COPY statement produces an error if a loaded string exceeds the target column length.
###################################################################################################################################
FORCE = TRUE | FALSE
Boolean that specifies to load all files, regardless of whether they’ve been loaded previously and have not changed since they were loaded. Note that this option reloads files, potentially duplicating data in a table.
###################################################################################################################################
LOAD_UNCERTAIN_FILES = TRUE | FALSE
Boolean that specifies to load files for which the load status is unknown. The COPY command skips these files by default
The load status is unknown if all of the following conditions are true:

The file’s LAST_MODIFIED date (i.e. date when the file was staged) is older than 64 days.
The initial set of data was loaded into the table more than 64 days earlier.
If the file was already loaded successfully into the table, this event occurred more than 64 days earlier.
###################################################################################################################################