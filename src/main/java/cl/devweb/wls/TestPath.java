package cl.devweb.wls;


import java.io.IOException;
import java.util.Date;

import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;




@WebServlet("/TestPath")
public class TestPath extends HttpServlet {

	private static final long serialVersionUID = 1L;
	private static final Logger LOGGER = LogManager.getLogger(TestPath.class);

    public TestPath() {
    }


    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

    	ServletContext context = request.getServletContext();
    	String path = context.getRealPath("/");

    	//LOGGER
		System.out.println("path = " + path);


	}


	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}

}
