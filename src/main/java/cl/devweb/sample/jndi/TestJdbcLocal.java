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
@WebServlet("/TestJdbcLocal")
public class TestJdbcLocal extends HttpServlet {
    private static final long serialVersionUID = 1L;

    /**
     * @see HttpServlet#HttpServlet()
     */
    public TestJdbcLocal() {
        super();
    }

    /**
     * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
     */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        response.getWriter().append("Served at: ").append(request.getContextPath());


        System.out.println("conectando...local\n");
        //String url = "t3://200.14.166.72:9071";  // apuntar a remote WLS - http://200.14.166.72:9071 - localhost:7001

        Context ctx;

        try {
            //local:
            ctx = new InitialContext();
            javax.sql.DataSource ds = (javax.sql.DataSource) ctx.lookup("JDBC/VENTA_CN");  // JDBC/VENTA_CN  VISTA_360_CN
            Connection conn = ds.getConnection();

            // Create Oracle DatabaseMetaData object
            DatabaseMetaData meta = conn.getMetaData();

            // gets driver info:
            System.out.println("\nLocal:\nJDBC driver version is " + meta.getDriverVersion());
            System.out.println("\nfecha:  " + new Date() );
            response.getWriter().append("local\nJDBC driver version is ").append(meta.getDriverVersion());
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
