#############################################################################
#
# @author Copyright (c) 2010 - 2011 by Middleware Magic, All Rights Reserved.
#
#############################################################################

# check domain.properties
# setDomainEnv
# java weblogic.WLST serverAdminState.py

from java.io import FileInputStream
 
propInputStream = FileInputStream("domain.properties")
configProps = Properties()
configProps.load(propInputStream)
 
domainName=configProps.get("domain.name")
adminURL=configProps.get("admin.url")
adminUserName=configProps.get("admin.userName")
adminPassword=configProps.get("admin.password")
totalServerToMonitor=configProps.get("totalServersToMonitor")
 
i=1
while (i <= int(totalServerToMonitor)) :
    url=configProps.get("server."+ str(i)+".url")
    connect(adminUserName,adminPassword,url)
    serverRuntime()
    state=cmo.getState()
    name=cmo.getName()
    if state == 'ADMIN' :
        print "ALERT::::::::Server Name: " + name + " Is currently in State: " + state
        try:
            print 'Resuming Server: .....'
            cmo.resume()
            print "Server: "+name +"Moved to State : " + cmo.getState()
        except:
            print "NOTE:::::::::Unable to Move Server: " + name + " To good State"
    else:
        print ''
        print ''
        print "GOOD::::::::> Server Name: " + name + " Is currently in State: " + state + '                     :)'
    i = i + 1
