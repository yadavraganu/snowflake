from snowconnect.snowconnect import Snow_Connect
import os
def Load_Into_Stage(k,v,root,logger):
    data_path=os.path.join(root,'data')
    if k.upper()=='INTERNAL':
        Stage_Name=v.split(':')[0]
        File_Name=v.split(':')[1]
        Actual_File_Path=os.path.join(data_path,File_Name)
        Put_Command="PUT "+"file://"+Actual_File_Path+" @"+Stage_Name+" OVERWRITE=TRUE AUTO_COMPRESS=TRUE"
        logger.info(Put_Command)
        Snow_Connect(Put_Command,logger)