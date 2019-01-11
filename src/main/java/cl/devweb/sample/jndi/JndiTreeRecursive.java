package cl.devweb.sample.jndi;

import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NameClassPair;
import javax.naming.NamingEnumeration;
import javax.naming.NamingException;

import org.apache.commons.collections4.MapUtils;

public class JndiTreeRecursive {


    public static void main(String[] args) throws Exception {

        System.out.println("start.");

        Properties env = new Properties();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "weblogic.jndi.WLInitialContextFactory");
        env.put(Context.SECURITY_PRINCIPAL, "weblogic");
        env.put(Context.SECURITY_CREDENTIALS, "welcome1");
        env.put(Context.PROVIDER_URL, " t3://127.0.0.1:7001/");
        Context context = new InitialContext(env);

        Map map = JndiTreeRecursive.toMap(context);
        //System.out.println(map);

        MapUtils.debugPrint(System.out, "myMap", map);
        System.out.println("end.");
    }



    public static Map toMap(Context ctx) throws NamingException {

        String namespace = ctx instanceof InitialContext ? ctx.getNameInNamespace() : "";
        HashMap<String, Object> map = new HashMap<String, Object>();
        System.out.println("> Listing namespace: " + namespace);
        NamingEnumeration<NameClassPair> list = ctx.list(namespace);
        while (list.hasMoreElements()) {
            NameClassPair next = list.next();
            String name = next.getName();
            String jndiPath = namespace + name;
            Object lookup;
            try {
                System.out.println("> Looking up name: " + jndiPath);
                Object tmp = ctx.lookup(jndiPath);
                if (tmp instanceof Context) {
                    lookup = toMap((Context) tmp);
                } else {
                    lookup = tmp.toString();
                }
            } catch (Throwable t) {
                lookup = t.getMessage();
            }
            map.put(name, lookup);

        }
        return map;
    }

}
