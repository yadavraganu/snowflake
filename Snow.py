#install python Snowflake Package using pip install --upgrade snowflake-connector-python
##pip install snowflake-ingest
import snowflake.connector,os,sys
from propertyreader.propertyreader import propertyreader
from snowconnect.snowconnect import Snow_Connect
from loadintostage.loadintostage import Load_Into_Stage,Cleanup_Stage
from snowpipe.snowpipe import create_ingester_manager
import logging
from datetime import datetime
from logging import getLogger
root=os.getcwd()
log_path=os.path.join(root,'logs','run_'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+".log")
logging.basicConfig(
        filename=log_path,
        format='%(asctime)s %(message)s',
        level=logging.INFO)
logger = getLogger()
operation=sys.argv[1]

if operation=='Read_Data':
    z=propertyreader(root,operation,logger)
    for x in z:
        Snow_Connect(x,logger)
elif operation=='Load_Into_Stage':
    z=propertyreader(root,operation,logger)
    for x in z:
        k=x[0]
        v=x[1]
        Load_Into_Stage(k,v,root,logger)
elif operation=='Cleanup_Stage':
    z=propertyreader(root,operation,logger)
    for x in z:
        k=x[0]
        v=x[1]
        Cleanup_Stage(k,v,root,logger)        
elif operation=='Trigger_Pipe_Ingest':
    z=propertyreader(root,operation,logger)
    for x in z:
        pipe=x[0]
    create_ingester_manager(root,pipe)
            

    

