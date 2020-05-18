package cl.devweb.ssl;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

/**
 * Servlet implementation class TestHttps
 */
@WebServlet("/TestHttps")
public class TestHttps extends HttpServlet {
	private static final long serialVersionUID = 1L;

    /**
     * @see HttpServlet#HttpServlet()
     */
    public TestHttps() {
        super();
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());

		RestTemplate restTemplate = new RestTemplate();

		String fooResourceUrl = "http://127.0.0.1:7002/jwt-service/jwt/certificate";
		//String fooResourceUrl = "https://www.google.com/";


		ResponseEntity<String> responseEntity  = restTemplate.getForEntity(fooResourceUrl , String.class);  // + "/1"

		System.out.println("=" + responseEntity);
		//assertThat(response.getStatusCode(), equalTo(HttpStatus.OK));

	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}

}
