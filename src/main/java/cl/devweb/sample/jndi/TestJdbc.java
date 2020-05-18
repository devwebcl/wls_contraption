package cl.devweb.sample.jndi;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.SQLException;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class TestJdbc
 */
public class TestJdbc extends HttpServlet {
    private static final long serialVersionUID = 1L;

    /**
     * @see HttpServlet#HttpServlet()
     */
    public TestJdbc() {
        super();
    }

    /**
     * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
     */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        response.getWriter().append("Served at: ").append(request.getContextPath());

        // from https://docs.oracle.com/cd/B28359_01/java.111/b31224/getsta.htm
        Context ctx;
        try {
            ctx = new InitialContext();

            javax.sql.DataSource ds = (javax.sql.DataSource) ctx.lookup("JDBC/my_datasource");
            Connection conn = ds.getConnection();

            // Create Oracle DatabaseMetaData object
            DatabaseMetaData meta = conn.getMetaData();

            // gets driver info:
            System.out.println("JDBC driver version is " + meta.getDriverVersion());
            response.getWriter().append("\nJDBC driver version is ").append(meta.getDriverVersion());

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
