#############################################################################
# Test Datasources on a domain
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 2.1, 2016-10-04
#
#############################################################################
# Modify these values as necessary
  
# @ggonzalez:
# adminServerName=AdminServer
# java weblogic.WLST testDS.py -loadProperties testDS.properties 

import sys, traceback
scriptName = sys.argv[0]
#
#
lineSeperator='__________________________________________________________________________________'
#
#
def usage():
  print 'Call script as: '
  print 'Windows: wlst.cmd '+scriptName+' -loadProperties testDS.properties'
  print 'Linux: wlst.sh '+scriptName+' -loadProperties environment.properties'
  print 'Property file should contain the following properties: '
  print "adminUrl=hhs-sbm3015:7001"
  print "adminUser=weblogic"
  print "adminPwd=welcome1"
#
#
def connectToadminServer(adminUrl, adminServerName):
  print(lineSeperator)
  print('Try to connect to the AdminServer')
  try:
    connect(userConfigFile=usrCfgFile, userKeyFile=usrKeyFile, url=adminUrl)
  except NameError, e:
    print('Apparently user config properties usrCfgFile and usrKeyFile not set.')
    print('Try to connect to the AdminServer adminUser and adminPwd properties')
    connect(adminUser, adminPwd, adminUrl)
#
#
def main():
  try:
    pad='                                                                               '
    print(lineSeperator)
    print('Check datasources for domain')
    print(lineSeperator)
    print ('Connect to the AdminServer: '+adminServerName)
    connectToadminServer(adminUrl, adminServerName)
    print(lineSeperator)
    allServers=domainRuntimeService.getServerRuntimes();
    if (len(allServers) > 0):
      for tempServer in allServers:
        jdbcServiceRT = tempServer.getJDBCServiceRuntime();
        dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans();
        print('\nServer '+tempServer.getName())
        if (len(dataSources) > 0):
          print('Datasource                                                  '[:30]+'\tState\tTest')
          for dataSource in dataSources:
            testPool = dataSource.testPool()
            dataSourceName = dataSource.getName()+pad
            dataSourceNamePad=dataSourceName[:30]
            if (testPool == None):
              print dataSourceNamePad+'\t'+dataSource.getState()+'\tOK'
            else:
              print dataSourceNamePad+'\t'+dataSource.getState()+'\tFailure: '
              print testPool
    print(lineSeperator)
    print('Done...')
    print(lineSeperator)
  except NameError, e:
    print('Apparently properties not set.')
    print "Please check the property: ", sys.exc_info()[0], sys.exc_info()[1]
    usage()
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
#
main();
