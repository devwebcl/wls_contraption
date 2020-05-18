package cl.devweb.hello;


import java.io.IOException;
import java.util.Enumeration;
import java.util.Properties;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class TestJavaProps
 * properties
 */
@WebServlet("/TestJavaProps")
public class TestJavaProps extends HttpServlet {
    private static final long serialVersionUID = 1L;

    /**
     * @see HttpServlet#HttpServlet()
     */
    public TestJavaProps() {
        super();
    }

    /**
     * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
     */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        System.out.println("properties:");
        response.getWriter().append("properties:\n");

        Properties p = System.getProperties();
        Enumeration keys = p.keys();
        while (keys.hasMoreElements()) {
            String key = (String)keys.nextElement();
            String value = (String)p.get(key);
            response.getWriter().append(key + ": " + value + "\n");
            System.out.println(key + ": " + value);
        }

        response.getWriter().append("Served at: ").append(request.getContextPath());
    }

    /**
     * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
     */
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        doGet(request, response);
    }

}
