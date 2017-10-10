
java weblogic.Deployer -adminurl t3://127.0.0.1:7001 -username weblogic -password welcome1 -deploy shared-lib-ome-war.war -library
java weblogic.Deployer -adminurl t3://127.0.0.1:7001 -username weblogic -password welcome1 -deploy shared-lib-two-war.war -library
java weblogic.Deployer -adminurl t3://127.0.0.1:7001 -username weblogic -password welcome1 -deploy shared-lib-three-war.war -library

java weblogic.Deployer -adminurl t3://127.0.0.1:7001 -username weblogic -password welcome1 -deploy micro-service.war
java weblogic.Deployer -adminurl t3://127.0.0.1:7001 -username weblogic -password welcome1 -deploy sample-listener.ear


