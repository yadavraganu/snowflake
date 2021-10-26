CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
  [ { WAREHOUSE = <string> } | { USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> } ]
  [ SCHEDULE = '{ <num> MINUTE | USING CRON <expr> <time_zone> }' ]
  [ ALLOW_OVERLAPPING_EXECUTION = TRUE | FALSE ]
  [ <session_parameter> = <value> [ , <session_parameter> = <value> ... ] ]
  [ USER_TASK_TIMEOUT_MS = <num> ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ AFTER <string> ]
[ WHEN <boolean_expr> ]
AS
  <sql>
#################################################################################################################################  
<name>--String that specifies the identifier (i.e. name) for the task; must be unique for the schema in which the task is created.
#################################################################################################################################
<sql>--Any single SQL statement, or a call to a stored procedure, executed when the task runs.
#################################################################################################################################
WAREHOUSE = <string> --Specifies the virtual warehouse that that provides compute resources for task runs.

USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> --Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size. Once a task has successfully completed a few runs, Snowflake ignores this parameter setting.If a WAREHOUSE = string parameter value is specified, then setting this parameter produces a user error.
#################################################################################################################################
SCHEDULE = USING CRON expr time_zone | num MINUTE
The maximum supported value is 11520 (8 days). Tasks that have a greater num MINUTE value never run.
A schedule must be defined for a standalone task or the root task in a task tree, or the task will never run.
A schedule cannot be specified for child tasks in a task tree (i.e. tasks that have a predecessor task set using the AFTER parameter).
#################################################################################################################################
ALLOW_OVERLAPPING_EXECUTION = TRUE | FALSE
This parameter can only be set on a root task. The setting applies to all tasks in the tree.
The parameter can be set on standalone tasks but does not affect the task behavior. Snowflake ensures only one instance of a standalone task is running at a given time.
TRUE ensures only one instance of a root task is running at a given time. If a root task is still running when the next scheduled run time occurs, then that scheduled time is skipped. This guarantee does not extend to child tasks. If the next scheduled run of the root task occurs while the current run of a child task is still in operation, another instance of the task tree begins.
FALSE ensures only one instance of a particular tree of tasks is allowed to run at a time. The next run of a root task is scheduled only after all child tasks in the tree have finished running. This means that if the cumulative time required to run all tasks in the tree exceeds the explicit scheduled time set in the definition of the root task, at least one run of the task tree is skipped.
#################################################################################################################################

session_parameter = <value> [ , session_parameter = <value> ... ]
Specifies a comma-separated list of session parameters to set for the session when the task runs. A task supports all session parameters. For the complete list

#################################################################################################################################
USER_TASK_TIMEOUT_MS = <num>
Specifies the time limit on a single run of the task before it times out (in milliseconds).
Default: 3600000 (1 hour)

#################################################################################################################################
COPY GRANTS

Specifies to retain the access permissions from the original task when a new task is created using any of the following CREATE TASK variants:
CREATE OR REPLACE TASK
CREATE TASK … CLONE

#################################################################################################################################

COMMENT = <'string_literal'>
Specifies a comment for the task.

#################################################################################################################################
AFTER <string>

Specifies the predecessor task for the current task. When a run of the predecessor task finishes successfully, it triggers this task (after a brief lag).
Accounts are currently limited to a maximum of 10000 resumed tasks.
Snowflake guarantees that at most one instance of a task with a defined schedule is running at a given time; however, we cannot provide the same guarantee for tasks with a defined predecessor task.
#################################################################################################################################
WHEN <boolean_expr>
Specifies a Boolean SQL expression; multiple conditions joined with AND/OR are supported. When a task is triggered (based on its SCHEDULE or AFTER setting), it validates the conditions of the expression to determine whether to execute. If the conditions of the expression are not met, then the task skips the current run. Any tasks that identify this task as a predecessor also do not run.

Currently, only the following function is supported for evaluation in the SQL expression:
SYSTEM$STREAM_HAS_DATA
Indicates whether a specified stream contains change tracking data. Used to skip the current task run if the stream contains no change data.
#################################################################################################################################

To abort the run of the specified task, execute the SYSTEM$USER_TASK_CANCEL_ONGOING_EXECUTIONS function



#################################################################################################################################

CREATE TASK t1
  SCHEDULE = 'USING CRON 0 9-17 * * SUN America/Los_Angeles'
  TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24'
  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
AS
INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);

CREATE TASK mytask_hour
  WAREHOUSE = mywh
  SCHEDULE = 'USING CRON 0 9-17 * * SUN America/Los_Angeles'
  TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24'
AS
INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
CREATE TASK mytask_minute
  WAREHOUSE = mywh
  SCHEDULE = '5 MINUTE'
AS
INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);

CREATE TASK mytask1
  WAREHOUSE = mywh
  SCHEDULE = '5 minute'
WHEN
  SYSTEM$STREAM_HAS_DATA('MYSTREAM')
AS
  INSERT INTO mytable1(id,name) SELECT id, name FROM mystream WHERE METADATA$ACTION = 'INSERT';
  
CREATE TASK mytask2
  WAREHOUSE = mywh
  AFTER mytask1
AS
INSERT INTO mytable2(id,name) SELECT id, name FROM mytable1;