# connect('weblogic','welcome1', 't3://127.0.0.1:7001');
connect('weblogic','welcome1', 't3://200.14.166.72:9071');


servers = domainRuntimeService.getServerRuntimes();
for server in servers:
    print 'SERVER: ' + server.getName();

    print('APPLICATION RUNTIME INFORMATION');
    apps = server.getApplicationRuntimes();
    for app in apps:
        print 'Application: ' + app.getName();
        crs = app.getComponentRuntimes();
        for cr in crs:
            print '-Component Type: ' + cr.getType();
            if (cr.getType() == 'EJBComponentRuntime'):
                ejbRTs = cr.getEJBRuntimes();
                for ejbRT in ejbRTs:
                    print ' -EJBRunTime: ' + ejbRT.getName() + ' Type ' + ejbRT.getType();
                    if (ejbRT.getType() == 'MessageDrivenEJBRuntime'):
                        print '  -MDB Status: ' + ejbRT.getMDBStatus() + ', MDB Health State: ' + repr(ejbRT.getHealthState());
                    if (ejbRT.getType() == 'StatelessEJBRuntime'):
                        print '  -EJB Name: ' + ejbRT.getEJBName();
                        print '  -Resources: ' + repr(ejbRT.getTransactionRuntime());
            if (cr.getType() == 'WebAppComponentRuntime'):
                print ' -Name: ' + cr.getName() + ', Session Current Count: ' + repr(cr.getOpenSessionsCurrentCount());
                servlets = cr.getServlets();
                for servlet in servlets:
                    print '  -Servlet: ' + servlet.getServletName() + ', total: ' + repr(servlet.getInvocationTotalCount()) + ', average time: ' + repr(servlet.getExecutionTimeAverage());

    print('JMS RUNTIME INFORMATION');
    jmsRuntime = server.getJMSRuntime();
    connections = jmsRuntime.getConnections();
    for connection in connections:
        print('-Connection Name: ' + connection.getName());
        sessions = connection.getSessions();
        for session in sessions:
            print(' -Session Name: ' + session.getName());
            consumers = session.getConsumers();
            for consumer in consumers:
                print('  -Consumer Name: ' + consumer.getName() + ', Bytes Received: ' + repr(consumer.getBytesReceivedCount()));
            producers = session.getProducers();
            for producer in producers:
                print('  -Producer Name: ' + producer.getName() + ', Bytes Send: ' + repr(producer.getBytesSentCount()));
    jmsServers = jmsRuntime.getJMSServers();
    for jmsServer in jmsServers:
        print('-JMSServer: ' + jmsServer.getName());
        destinations = jmsServer.getDestinations();
        for destination in destinations:
            print(' -Destination: ' + destination.getName() + ', ' + repr(destination.getMessagesHighCount()) + ', ' + repr(destination.getConsumersHighCount()));

    print('JDBC RUNTIME INFORMATION');
    jdbcRuntime = server.getJDBCServiceRuntime();
    datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans();
    for datasource in datasources:
        print('-Data Source: ' + datasource.getName() + ', Active Connections: ' + repr(datasource.getActiveConnectionsCurrentCount()) + ', Waiting for Connections: ' + repr(datasource.getWaitingForConnectionCurrentCount()));

