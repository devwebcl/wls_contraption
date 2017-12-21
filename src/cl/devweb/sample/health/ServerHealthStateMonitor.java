package cl.devweb.sample.health;

import weblogic.management.mbeanservers.domainruntime.DomainRuntimeServiceMBean;
import weblogic.management.runtime.ServerRuntimeMBean;
import javax.management.MBeanServerConnection;
import javax.management.MalformedObjectNameException;
import javax.management.ObjectName;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;
import javax.naming.Context;

//import com.google.common.collect.HashBasedTable;
//import com.google.common.collect.Table;

import weblogic.management.jmx.MBeanServerInvocationHandler;

import java.util.Date;
import java.util.Hashtable;
import java.util.Map;
import java.util.Set;
import java.io.IOException;
import java.net.MalformedURLException;
import weblogic.management.runtime.JDBCDataSourceRuntimeMBean;
import javax.management.*;
import javax.naming.*;

// https://docs.oracle.com/cd/E57014_01/wls/WLAPI/weblogic/management/mbeanservers/domainruntime/DomainRuntimeServiceMBean.html
// from http://middlewaremagic.com/weblogic/?p=2851

public class ServerHealthStateMonitor {
    private static MBeanServerConnection connection;
    private static JMXConnector connector;
    private static final ObjectName service;
    private static String combea = "com.bea:Name=";
    private static String service1 = "DomainRuntimeService,Type=weblogic.management.mbeanservers.domainruntime.DomainRuntimeServiceMBean";
    private static String service2 = "RuntimeService,Type=weblogic.management.mbeanservers.runtime.RuntimeServiceMBean";

    static {
        try {
            service = new ObjectName(combea + service1);
        } catch (MalformedObjectNameException e) {
            throw new AssertionError(e.getMessage());
        }
    }

    public static void initConnection(String hostname, String portString, String username, String password)
            throws IOException, MalformedURLException {
        String protocol = "t3";
        Integer portInteger = Integer.valueOf(portString);
        int port = portInteger.intValue();
        String jndiroot = "/jndi/";
        String mserver = "weblogic.management.mbeanservers.domainruntime";
        JMXServiceURL serviceURL = new JMXServiceURL(protocol, hostname, port, jndiroot + mserver);
        Hashtable h = new Hashtable();
        h.put(Context.SECURITY_PRINCIPAL, username);
        h.put(Context.SECURITY_CREDENTIALS, password);
        h.put(JMXConnectorFactory.PROTOCOL_PROVIDER_PACKAGES, "weblogic.management.remote");
        connector = JMXConnectorFactory.connect(serviceURL, h);
        connection = connector.getMBeanServerConnection();
    }

    public static ObjectName[] getServerRuntimes() throws Exception {
        return (ObjectName[]) connection.getAttribute(service, "ServerRuntimes");
    }

    public void printNameAndState() throws Exception {
        ObjectName arr[] = getServerRuntimes();
        for (ObjectName temp : arr)
            System.out.println("-> servers: " + temp);
        ObjectName domain = (ObjectName) connection.getAttribute(service, "DomainConfiguration");
        System.out.println("Domain: " + domain.toString());
        ObjectName[] servers = (ObjectName[]) connection.getAttribute(domain, "Servers");
        for (ObjectName server : servers) {
            String aName = (String) connection.getAttribute(server, "Name");
            try {
                ObjectName ser = new ObjectName("com.bea:Name=" + aName + ",Location=" + aName + ",Type=ServerRuntime");
                String serverState = (String) connection.getAttribute(ser, "State");
                System.out.println("-> Server: " + aName + " - State: " + serverState);
                weblogic.health.HealthState serverHealthState = (weblogic.health.HealthState) connection
                        .getAttribute(ser, "HealthState");
                int hState = serverHealthState.getState();
                if (hState == weblogic.health.HealthState.HEALTH_OK)
                    System.out.println("+ Server: " + aName + " - State Health: HEALTH_OK");
                if (hState == weblogic.health.HealthState.HEALTH_WARN)
                    System.out.println("+ Server: " + aName + " - State Health: HEALTH_WARN");
                if (hState == weblogic.health.HealthState.HEALTH_CRITICAL)
                    System.out.println("+ Server: " + aName + " - State Health: HEALTH_CRITICAL");
                if (hState == weblogic.health.HealthState.HEALTH_FAILED)
                    System.out.println("+ Server: " + aName + " - State Health: HEALTH_FAILED");
                if (hState == weblogic.health.HealthState.HEALTH_OVERLOADED)
                    System.out.println("+ Server: " + aName + " - State Health: HEALTH_OVERLOADED");
            } catch (javax.management.InstanceNotFoundException e) {
                System.out.println("-> Server: " + aName + " - State: SHUTDOWN (or Not Reachable)");
            }
        }
    }

    public static void main(String[] args) throws Exception {
        String hostname = "127.0.0.1";
        String portString = "7001";
        String username = "weblogic";
        String password = "welcome1";
        ServerHealthStateMonitor s = new ServerHealthStateMonitor();
        initConnection(hostname, portString, username, password);
        s.printNameAndState();
        connector.close();
    }

    /*
    public static void main(String[] args) throws Exception {

        System.out.println("Starting...  " + new Date() );

        Table<String, String, String> domainCredentials = HashBasedTable.create();

        //Guava Table:
        domainCredentials.put(DOMAIN1, HOSTNAME, "127.0.0.1");
        domainCredentials.put(DOMAIN1, PORT, "40000");
        domainCredentials.put(DOMAIN1, USERNAME, "weblogic");
        domainCredentials.put(DOMAIN1, PASSWORD, "welcome1");

        domainCredentials.put(DOMAIN2, HOSTNAME, "127.0.0.1");
        domainCredentials.put(DOMAIN2, PORT, "10000");
        domainCredentials.put(DOMAIN2, USERNAME, "weblogic");
        domainCredentials.put(DOMAIN2, PASSWORD, "welcome1");

        domainCredentials.put(DOMAIN3, HOSTNAME, "127.0.0.1");
        domainCredentials.put(DOMAIN3, PORT, "20000");
        domainCredentials.put(DOMAIN3, USERNAME, "weblogic");
        domainCredentials.put(DOMAIN3, PASSWORD, "welcome1");

        domainCredentials.put(DOMAIN4, HOSTNAME, "127.0.0.1");
        domainCredentials.put(DOMAIN4, PORT, "30000");
        domainCredentials.put(DOMAIN4, USERNAME, "weblogic");
        domainCredentials.put(DOMAIN4, PASSWORD, "welcome1");


        Set<String> dominios = domainCredentials.rowKeySet();

        for(String i : dominios) {

            Map<String, String> cred = domainCredentials.row(i);
            System.out.println(">>"+cred);

            String hostname = cred.get(HOSTNAME);
            String portString = cred.get(PORT);
            String username =  cred.get(USERNAME);
            String password = cred.get(PASSWORD);

            ServerHealthStateMonitor s = new ServerHealthStateMonitor();
            initConnection(hostname, portString, username, password);
            s.printNameAndState();
            connector.close();

            System.out.println();

        }*/



}
