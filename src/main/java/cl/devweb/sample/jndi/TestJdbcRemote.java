package cl.devweb.sample.jndi;


import java.io.IOException;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.SQLException;
import java.util.Date;
import java.util.Hashtable;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class TestJdbc
 */
@WebServlet("/TestJdbcRemote")
public class TestJdbcRemote extends HttpServlet {
    private static final long serialVersionUID = 1L;

    /**
     * @see HttpServlet#HttpServlet()
     */
    public TestJdbcRemote() {
        super();
    }

    /**
     * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
     */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.getWriter().append("Served at: ").append(request.getContextPath());


        System.out.println("conectando...remote\n");
        String url = "t3://200.14.166.72:9071";  // apuntar a remote WLS - http://200.14.166.72:9071 - localhost:7001

        //Context ctx;
        java.sql.Connection conn = null;

        try {
            //remote:
            Context ctx = null;
            Hashtable<String, String> ht = new Hashtable<String, String>();
            ht.put(Context.INITIAL_CONTEXT_FACTORY, "weblogic.jndi.WLInitialContextFactory");
            ht.put(Context.PROVIDER_URL, url);
            ht.put(Context.SECURITY_PRINCIPAL, "weblogic");
            ht.put(Context.SECURITY_CREDENTIALS, "welcome1");

            ctx = new InitialContext(ht);
            javax.sql.DataSource ds = (javax.sql.DataSource) ctx.lookup("JDBC/VISTA_360_CN");
            conn = ds.getConnection();
            conn.setAutoCommit(true);

            // Create Oracle DatabaseMetaData object
            DatabaseMetaData meta = conn.getMetaData();

            // gets driver info:
            System.out.println("\nRemote:\nJDBC driver version is " + meta.getDriverVersion());
            System.out.println("\nfecha:  " + new Date() );
            response.getWriter().append("\nJDBC driver version is ").append(meta.getDriverVersion());
            response.getWriter().append("\nfecha: ").append(""+ new Date());

        } catch (NamingException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            e.printStackTrace();
        }


    }

    /**
     * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
     */
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        doGet(request, response);
    }

}
