#############################################################################
#
# @author Copyright (c) 2010 - 2011 by Middleware Magic, All Rights Reserved.
#
#############################################################################
 
from java.io import FileInputStream
 
propInputStream = FileInputStream("createMultipleDataSource.properties")
configProps = Properties()
configProps.load(propInputStream)
 
domainName=configProps.get("domain.name")
adminURL=configProps.get("admin.url")
adminUserName=configProps.get("admin.userName")
adminPassword=configProps.get("admin.password")
 
totalDataSource_to_Create=configProps.get("total.DS")
 
connect(adminUserName, adminPassword, adminURL)
edit()
startEdit()
print '========================================='
print 'Creating DataSource....'
print '========================================='
i=1
while (i <= int(totalDataSource_to_Create)) :
 
    try:
        cd('/')
        dsName=configProps.get("datasource.name."+ str(i))
        dsFileName=configProps.get("datasource.filename."+ str(i))
        dsDatabaseName=configProps.get("datasource.database.name."+ str(i))
        datasourceTarget=configProps.get("datasource.target."+ str(i))
        dsJNDIName=configProps.get("datasource.jndiname."+ str(i))
        dsDriverName=configProps.get("datasource.driver.class."+ str(i))
        dsURL=configProps.get("datasource.url."+ str(i))
        dsUserName=configProps.get("datasource.username."+ str(i))
        dsPassword=configProps.get("datasource.password."+ str(i))
        dsTestQuery=configProps.get("datasource.test.query."+ str(i))
        dsGlobalTx=configProps.get("datasource.globaltx."+ str(i))

        print ''
        print 'Creating DataSource: ',dsName,' ....'

        cmo.createJDBCSystemResource(dsName)
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
        cmo.setName(dsName)
 
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
        # set('JNDINames',jarray.array([String('jdbc/' + dsName )], String))
        set('JNDINames', jarray.array([String(dsJNDIName)], String))
 
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName )
        cmo.setUrl(dsURL)
        cmo.setDriverName( dsDriverName )
        cmo.setPassword(dsPassword)
 
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName )
        cmo.setTestTableName(dsTestQuery)
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
        cmo.createProperty('user')
 
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
        cmo.setValue(dsUserName)
 
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
        cmo.createProperty('databaseName')
 
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/databaseName')
        cmo.setValue(dsDatabaseName)
 
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
        cmo.setGlobalTransactionsProtocol(dsGlobalTx)
 
        cd('/SystemResources/' + dsName )
        set('Targets',jarray.array([ObjectName('com.bea:Name=' + datasourceTarget + ',Type=Server')], ObjectName))
 
        print 'DataSource: ',dsName,', has been created Successfully !!!'
        print ''
 
    except:
        print '***** CANNOT CREATE DATASOURCE !!! Check If the DataSource With the Name : ' , dsName ,' Already exists or NOT...'
        print ''
    i = i + 1
print '========================================='
save()
activate()

