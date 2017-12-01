#========================================
# WLST Script purpose: Configuring JMS Module
# Author: Pavan Devarakonda
# Update date: 3rd Aug 2017
#========================================
from java.util import Properties
from java.io import FileInputStream
from java.io import File
from java.io import FileOutputStream
from java import io
from java.lang import Exception
from java.lang import Throwable
import os.path
import sys
 
envproperty=""
if (len(sys.argv) > 1):
        envproperty=sys.argv[1]
else:
        print "Environment Property file not specified"
        sys.exit(2)
 
propInputStream=FileInputStream(envproperty)
configProps=Properties()
configProps.load(propInputStream)
 
##########################################
# Create JMS Moudle will take the 
# arguments as name, subdeployment name
# target can be on admin or managed server or cluster
##########################################
def createJMSModule(jms_module_name, adm_name, subdeployment_name):
        cd('/JMSServers')
        jmssrvlist=ls(returnMap='true')
        print jmssrvlist
        cd('/')
        module = create(jms_module_name, "JMSSystemResource")
        #cluster = getMBean("Clusters/"+cluster_target_name)
        #module.addTarget(cluster)
        #adm_name=get('AdminServerName')
        adm=getMBean("Servers/"+adm_name)
        module.addTarget(adm)
        cd('/SystemResources/'+jms_module_name)
 
        module.createSubDeployment(subdeployment_name)
        cd('/SystemResources/'+jms_module_name+'/SubDeployments/'+subdeployment_name)
        list=[]
        for j in jmssrvlist:
                s='com.bea:Name='+j+',Type=JMSServer'
                list.append(ObjectName(str(s)))
        set('Targets',jarray.array(list, ObjectName))
 
 
def getJMSModulePath(jms_module_name):
        jms_module_path = "/JMSSystemResources/"+jms_module_name+"/JMSResource/"+jms_module_name
        return jms_module_path
 
def createJMSTEMP(jms_module_name,jms_temp_name):
        jms_module_path= getJMSModulePath(jms_module_name)
        cd(jms_module_path)
        cmo.createTemplate(jms_temp_name)
        cd(jms_module_path+'/Templates/'+jms_temp_name)
        cmo.setMaximumMessageSize(20)
 
##########################################
# JMS Queu configuration function 
# arguments are : JMS module, 
# Queue name, jndi name
##########################################
def createJMSQ(jms_module_name,jndi,jms_queue_name):
        jms_module_path = getJMSModulePath(jms_module_name)
        cd(jms_module_path)
        cmo.createQueue(jms_queue_name)
        cd(jms_module_path+'/Queues/'+jms_queue_name)
        cmo.setJNDIName(jndi)
        cmo.setSubDeploymentName(subdeployment_name)
 
adminUser=configProps.get("adminUser")
adminPassword=configProps.get("adminPassword")
adminURL=configProps.get("adminURL")
 
connect(adminUser,adminPassword,adminURL)
#adm_name=get('AdminServerName')
adm_name=ls('Servers',returnMap='true')[0]
print adm_name
edit()
startEdit()
 
##########################################
#   JMS CONFIGURATION## 
##########################################
total_conf=configProps.get("total_conf")
tot_djmsm=configProps.get("total_default_jms_module")
#subdeployment_name=configProps.get("subdeployment_name")
 
a=1
while(a <= int(tot_djmsm)):
        i=int(a)
        jms_mod_name=configProps.get("jms_mod_name"+ str(i))
        #cluster=configProps.get("jms_mod_target"+ str(i))
        subdeployment_name=configProps.get("subdeployment_name"+ str(i))
        createJMSModule(jms_mod_name,adm_name,subdeployment_name)
        total_q=configProps.get("total_queue"+str(i))
        j=1
        while(j <= int(total_q)):
                queue_name=configProps.get("queue_name"+ str(i)+str(j))
                queue_jndi=configProps.get("queue_jndi"+ str(i)+str(j))
                createJMSQ(jms_mod_name,queue_jndi,queue_name)
                j = j + 1
        i=i+1
        a = a+1
save()
activate(block="true")
disconnect() 

