mvn clean
mvn package 

# mvn com.oracle.weblogic:weblogic-maven-plugin:undeploy
# mvn com.oracle.weblogic:weblogic-maven-plugin:deploy

java weblogic.Deployer -adminurl t3://127.0.0.1:7001 -username weblogic -password welcome1 -deploy -targets wls_cluster -name presentacion target/presentacion-0.3.2-SNAPSHOT.war -remote -upload



