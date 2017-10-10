from weblogic.security.internal import *  
from weblogic.security.internal.encryption import *

# source $DOMAIN_HOME/bin/setDomainEnv.sh
# cd $DOMAIN_HOME/security  

encryptionService = SerializedSystemIni.getEncryptionService(".")  
clearOrEncryptService = ClearOrEncryptedService(encryptionService)

passwd = raw_input("Enter encrypted password of one which you wanted to decrypt : ")

plainpwd = passwd.replace("\\", "")

print "Plain Text password is: " + clearOrEncryptService.decrypt(plainpwd) 

