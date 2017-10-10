#############################################################################
#
# @author Copyright (c) 2010 - 2011 by Middleware Magic, All Rights Reserved.
#
#############################################################################
 
from java.io import FileInputStream
 
propInputStream = FileInputStream("target_untarget_ds.properties")
configProps = Properties()
configProps.load(propInputStream)
 
userName = configProps.get("userName")
password = configProps.get("password")
adminUrl = configProps.get("admin.Url")
totalDsCount = configProps.get("total.Ds.Count")
 
connect(userName,password,adminUrl)
edit()
startEdit()
print ''
print '======================================================================'
print 'UnTargeting and Targeting of the DataSources has started.....'
print '======================================================================'
 
dsCount=1
while (dsCount <= int(totalDsCount)) :
    dsName = configProps.get("ds.Name."+ str(dsCount))
    tgName = configProps.get("target."+ str(dsCount))
    cd ('/JDBCSystemResources/'+ dsName)
    set('Targets',jarray.array([], ObjectName))
    print ''
    print 'DataSource = ', dsName ,', has been UnTargeted'
    set('Targets',jarray.array([ObjectName('com.bea:Name='+tgName+',Type=Cluster')], ObjectName))
    print 'Congrats!!! DataSource = ', dsName ,', now has been Targeted to "',tgName,'"'
    print ''
    dsCount = dsCount + 1
 
print '======================================================================'
print 'UnTrageting and Targeting of the DataSources has been completed !!!'
print '======================================================================'
print ''
 
activate()
exit()

