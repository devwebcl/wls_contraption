package cl.devweb.ssl;


import java.io.IOException;
import java.security.NoSuchAlgorithmException;

import javax.crypto.Cipher;
import javax.crypto.NoSuchPaddingException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class TestCrypto
 */
@WebServlet("/TestCrypto")
public class TestCrypto extends HttpServlet {
	private static final long serialVersionUID = 1L;

    /**
     * @see HttpServlet#HttpServlet()
     */
    public TestCrypto() {
        super();
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

		try {
			Cipher c = Cipher.getInstance("AES");
			System.out.println("max=" + c.getMaxAllowedKeyLength("AES") );

			response.getWriter().append("Served at: ").append(request.getContextPath());
			response.getWriter().append("max: ").append(""+ c.getMaxAllowedKeyLength("AES"));

		} catch (NoSuchAlgorithmException | NoSuchPaddingException e) {
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
