import commands
import os
import weblogic.security.internal.SerializedSystemIni
import weblogic.security.internal.encryption.ClearOrEncryptedService
import traceback
import sys
import getopt

from com.ziclix.python.sql import zxJDBC
from java.io import FileInputStream

intf = 'eth0'
intf_ip = commands.getoutput("/sbin/ip address show dev " + intf).split()
intf_ip = intf_ip[intf_ip.index('inet') + 1].split('/')[0]
print 'Using IP: ',intf_ip
var_user=''
var_pass=''

try:
        fh = open("resume.properties", "r")
        fh.close()
        print 'Using resume.properties'
        propInputStream = FileInputStream("resume.properties")
        configProps = Properties()
        configProps.load(propInputStream)
        var_user=configProps.get("userName")
        var_pass=configProps.get("passWord")
except IOError:
        try:
                opts, args = getopt.getopt(sys.argv[1:], "", ["username=", "password="])
                for o, a in opts:
                        if o == "--username":
                                var_user=a
                                print 'User: ',var_user
                        elif o == "--password":
                                var_pass=a
                                print 'Pass: ',var_pass
                        else:
                                assert False, "unhandled option"
        except getopt.GetoptError, err:
                print 'No -u and -p commandline arguments and no resume.properties...'
                var_user = raw_input("Enter user: ")
                var_pass = raw_input("Enter pass: ")

connect(var_user,var_pass,intf_ip+':7001')
rootdir=cmo.getRootDirectory()
secdir=rootdir+'/security'
allServers=domainRuntimeService.getServerRuntimes();
if (len(allServers) > 0):
  for tempServer in allServers:
    print 'Processing: ',tempServer.getName()
    jdbcServiceRT = tempServer.getJDBCServiceRuntime();
    dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans();
    if (len(dataSources) > 0):
                for dataSource in dataSources:
                        #print 'Resuming: ',dataSource.getName()
                        dataSource.resume()
                        dataSource.testPool()
                        cd('/JDBCSystemResources/' + dataSource.getName() + '/JDBCResource/' + dataSource.getName() + '/JDBCDriverParams/' + dataSource.getName() + '/Properties/' + dataSource.getName())
                        dbuser=cmo.lookupProperty('user').getValue()
                        #print 'User: ',dbuser
                        cd('/JDBCSystemResources/' + dataSource.getName() + '/JDBCResource/' + dataSource.getName() + '/JDBCDriverParams/' + dataSource.getName())
                        dburl=cmo.getUrl()
                        #print 'DbUrl: ',dburl
                        dbpassword=cmo.getPasswordEncrypted()
                        es=weblogic.security.internal.SerializedSystemIni.getEncryptionService(secdir)
                        ces=weblogic.security.internal.encryption.ClearOrEncryptedService(es)
                        dbpassword_decrypted=str(ces.decrypt("".join(map(chr, dbpassword))))
                        #print 'DbPassword: ',dbpassword_decrypted
                        dbdriver=cmo.getDriverName()
                        #print 'DbDriverName: ',dbdriver
                        try:
                                con=zxJDBC.connect(dburl,dbuser,dbpassword_decrypted,dbdriver)
                                cursor=con.cursor()
                                result=cursor.execute('select sysdate from dual')
                        except:
                                print 'ERROR: Url: ',dburl,' User: ',dbuser
                                traceback.print_exc()

                                