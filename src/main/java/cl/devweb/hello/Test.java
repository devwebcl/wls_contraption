package cl.devweb.hello;


import java.io.IOException;
import java.util.Date;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;



/**
 * Servlet implementation class Test
 */
@WebServlet("/Test")
public class Test extends HttpServlet {
	
	private static final long serialVersionUID = 1L;
	private static final Logger LOGGER = LogManager.getLogger(Test.class); 
	
    /**
     * Default constructor.
     */
    public Test() {
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub

		Date d = new Date();
		
		LOGGER.info("fecha {}", d);
		


		System.out.println("hola mundo");
		System.out.println("hola mundo fecha: " + d );
		System.out.println("log4j.configurationFile=" + System.getProperty("log4j.configurationFile"));

		
		response.getWriter().append("Served at: ").append(""+d+" ").append(request.getContextPath())
			.append(" \nweblogic.Name==" + System.getProperty("weblogic.Name"));

		// -Dweblogic.MuxerClass=weblogic.socket.NIOSocketMuxer
		System.out.println("weblogic.Name==" + System.getProperty("weblogic.Name") );

		System.out.println("weblogic.MuxerClass==" + System.getProperty("weblogic.MuxerClass") );

		System.out.println("weblogic.getImplementationVersion==" + Runtime.class.getPackage().getImplementationVersion() );
		System.out.println("weblogic.getSpecificationVersion==" + Runtime.class.getPackage().getSpecificationVersion() );

		java.awt.Image awtImg = java.awt.Toolkit.getDefaultToolkit().createImage("");
		System.out.println("awtImg="+awtImg);

	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
