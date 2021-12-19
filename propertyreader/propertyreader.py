import configparser
import os
def propertyreader(root,operation,logger):
    kv_list=[]
    config_path=os.path.join(root,'config','Snow_Input.ini')
    data_path=os.path.join(root,'data')
    parser=configparser.ConfigParser()
    parser.read(config_path)
    for section in parser.sections():
        if  section==operation:
            for k,v in parser.items(section):
                if section=='Load_Into_Stage':
                    logger.info("Reading {} Section........".format(section))
                    logger.info(k+" : "+v)
                    kv_list.append([k,v])
                elif section=='Read_Data':
                    logger.info("Reading {} Section........".format(section))
                    logger.info(k+" : "+v)
                    kv_list.append(v)
                elif section=='Trigger_Pipe_Ingest':
                    logger.info("Reading {} Section........".format(section))
                    logger.info(k+" : "+v)
                    kv_list.append(v.split(":"))
                elif section=='Cleanup_Stage':
                    logger.info("Reading {} Section........".format(section))
                    logger.info(k+" : "+v)
                    kv_list.append([k,v])    
    return kv_list                