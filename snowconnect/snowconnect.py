import snowflake.connector
import os
def Snow_Connect(Query,logger):
    ctx=snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    region=os.getenv('SNOWFLAKE_REGION')
    )
    cs = ctx.cursor()
    try:
        cs.execute(Query)
        one_row = cs.fetchone()
        logger.info("---------------------Query Result Start------------------------")
        logger.info(one_row)
        logger.info("---------------------Query Result End--------------------------")
    finally:
        cs.close()
        ctx.close()