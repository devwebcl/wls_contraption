#############################################################################
#
# @author Copyright (c) 2010 - 2011 by Middleware Magic, All Rights Reserved.
#
#############################################################################
 
from java.io import FileInputStream
import java.lang
import os
 
propInputStream = FileInputStream("domains.properties")
configProps = Properties()
configProps.load(propInputStream)
 
adminUrl = configProps.get("server.url")
adminUser = configProps.get("admin.username")
adminPassword = configProps.get("admin.password")
monitoringServerName = configProps.get("monitoring.server.name")
 
executeThread_Vs_HoggerThreadRatio = configProps.get("ExecuteThread_Vs_HoggerThreadRatio")
checkTimes_Number = configProps.get("checkTimes_Number")
checkInterval_in_Milliseconds = configProps.get("checkInterval_in_Milliseconds")
threadDumpTimes_Number = configProps.get("threadDumpTimes_Number")
threadDumpInterval_in_Milliseconds = configProps.get("threadDumpInterval_in_Milliseconds")
sendEmail_ThreadDump_Counter = configProps.get("sendEmail_ThreadDump_Counter")
 
i = 0
y = int(checkTimes_Number)
 
#############  This method would send the Alert Email with Thread Dump  #################
def sendMailThreadDump():
    # os.system('/bin/mailx -s  "ALERT: CHECK Thread Dumps as Hogger Thread Count Exceeded the Limit !!! " german.gonzalez@email.com < All_ThreadDump.txt')
    print '*********  ALERT MAIL HAS BEEN SENT  ******#################################################*****'
    print '*********  ALERT MAIL HAS BEEN SENT  ***********'
    print ''
 
#############  This method is checking the Hogger Threads Ratio  #################
def alertHoggerThreads(executeTTC , hoggerTC):
    print 'Execute Threads : ', executeTTC
    print 'Hogger Thread Count : ', hoggerTC
    print 'executeThread_Vs_HoggerThreadRatio :', executeThread_Vs_HoggerThreadRatio
    if hoggerTC != 0:
        ratio=(executeTTC/hoggerTC)
        print 'Ratio : ' , ratio
        print ''
        if (int(ratio) <= int(executeThread_Vs_HoggerThreadRatio)):
            print ' !!!! ALERT !!!! Stuck Threads are on its way.....'
            print ''
            message =  'ExecuteThreads Count= ' + str(executeTTC) + '   HoggingThreads= '+ str(hoggerTC) +'   ExecuteThreads/HoggingThreads Ratio= '+ str(ratio)
            cmd = "echo " + message +" > rw_file"
            os.system(cmd)
            genrateThreadDump()
        else:
            print '++++++++++++++++++++++++++++++++++++'
            print 'Everything is working fine till now'
            print '++++++++++++++++++++++++++++++++++++'
    else:
        print '++++++++++++++++++++++++++++++++++++'
        print 'Everything is working fine till now'
        print '++++++++++++++++++++++++++++++++++++'
 
#############  This method is Taking the Thread Dumps #################
def genrateThreadDump():
    b = int(sendEmail_ThreadDump_Counter)
    a = 0
    p = 0
    q = int(threadDumpTimes_Number)
    serverConfig()
    cd ('Servers/'+ monitoringServerName)
    while (p < q):
        if a < b:
            print 'Taking Thread Dump : ', p
            threadDump()
            cmd = "cat Thread_Dump_MS-3.txt >> All_ThreadDump.txt"
            os.system(cmd)
            print 'Thread Dump Collected : ', p ,' now Sleeping for ', int(threadDumpInterval_in_Milliseconds) , ' Seconds ...'
            print ''
            Thread.sleep(int(checkInterval_in_Milliseconds))
            b = b - 1
            p = p + 1
    sendMailThreadDump()
    cmd = "rm -f All_ThreadDump.txt"
    os.system(cmd)
    serverRuntime()
 
connect(adminUser,adminPassword,adminUrl)
serverRuntime()
cd('ThreadPoolRuntime/ThreadPoolRuntime')
 
while (i < y):
    executeTTC=cmo.getExecuteThreadTotalCount();
    hoggerTC=cmo.getHoggingThreadCount();
    alertHoggerThreads(executeTTC , hoggerTC)
    print 'Sleeping for ', int(checkInterval_in_Milliseconds) , ' ...'
    print ''
    Thread.sleep(int(checkInterval_in_Milliseconds))
    i = i + 1