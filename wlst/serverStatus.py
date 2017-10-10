username = 'weblogic'
password = 'welcome1'
URL='t3://localhost:7001'
connect(username,password,URL)
domainRuntime()
cd('ServerRuntimes')
servers=domainRuntimeService.getServerRuntimes()
for server in servers:
 print'SERVER NAME :',server.getName()
 print'SERVER STATE :',server.getState()
 print'SERVER LISTEN ADDRESS :',server.getListenAddress()
 print'SERVER LISTEN PORT :',server.getListenPort()
 print'SERVER HEALTH STATE :',server.getHealthState()

