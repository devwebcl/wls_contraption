from java.util import Properties
from java.io import FileInputStream
from java.io import File
from java import io
from java.lang import Exception
from java.lang import Throwable
import os.path
import sys
 
def createFlstr(fstr_name,dir_name,target_name):
        cd('/')
        fst = create(fstr_name, "FileStore")
        cd('/FileStores/'+fstr_name)
        cmo.setDirectory(dir_name)
        fst.addTarget(getMBean("/Servers/"+target_name))
 
def createJDstr(jstr_name,ds_name,target_name,prefix):
        cd('/')
        jst = create(jstr_name, "JDBCStore")
        cd('/JDBCStores/'+jstr_name)
        cmo.setDataSource(getMBean('/SystemResources/'+ds_name))
        cmo.setPrefixName(prefix)
        jst.addTarget(getMBean("/Servers/"+target_name))
 
def createJMSsrvr(jms_srv_name,target_name,persis_store,page_dir, thrs_high, thrs_low, msg_size):
        cd('/')
        srvr = create(jms_srv_name, "JMSServer")
        cd('/Deployments/'+jms_srv_name)
        srvr.setPersistentStore(getMBean('/FileStores/'+persis_store))
#       srvr.setPersistentStore(getMBean('/JDBCStores/'+persis_store))
        srvr.setPagingDirectory(page_dir)
        srvr.addTarget(getMBean("/Servers/"+target_name))
        srvr.setBytesThresholdLow(long(thrs_low))
        srvr.setBytesThresholdHigh(long(thrs_high))
        srvr.setMaximumMessageSize(long(msg_size))
 
envproperty=""
if (len(sys.argv) > 1):
    envproperty=sys.argv[1]
else:
    print "Environment Property file not specified"
    sys.exit(2)
propInputStream=FileInputStream(envproperty)
configProps=Properties()
configProps.load(propInputStream)
 
adminUser=configProps.get("adminUser")
adminPassword=configProps.get("adminPassword")
adminURL=configProps.get("adminURL")
 
connect(adminUser,adminPassword,adminURL)
 
edit()
startEdit()
 
#=============# JMS SERVER and PERSISITENT STORE CONFIGURATION #=============#
total_fstore=configProps.get("total_fstore")
#total_jstore=configProps.get("total_jstore")
total_jmssrvr=configProps.get("total_jmssrvr")
 
j=1
while (j <= int(total_jmssrvr)):
        jms_srv_name=configProps.get("jms_srvr_name"+ str(j))
        trg=configProps.get("jms_srvr_target"+ str(j))
        persis_store=configProps.get("jms_srvr_persis_store_name"+str(j))
        page_dir=configProps.get("jms_srvr_pag_dir"+str(j))
        thrs_high=configProps.get("jms_srvr_by_threshold_high"+str(j))
        thrs_low=configProps.get("jms_srvr_by_threshold_low"+str(j))
        msg_size=configProps.get("jms_srvr_max_msg_size"+str(j))
        createFlstr(persis_store,page_dir,trg)
        createJMSsrvr(jms_srv_name,trg,persis_store,page_dir,thrs_high,thrs_low,msg_size)
        j = j+1
#==========================================================================================#
save()
activate()
