package cl.devweb.ssl;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import javax.net.ssl.SSLHandshakeException;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;

public class SSLPoke
{
  public static void main(String[] paramArrayOfString)
  {
    if (paramArrayOfString.length != 2)
    {
      System.err.println("Utility to debug Java connections to SSL servers");
      System.err.println("Usage: ");
      System.err.println("  java " + SSLPoke.class.getName() + " <host> <port>");
      System.err.println("or for more debugging:");
      System.err.println("  java -Djavax.net.debug=ssl " + SSLPoke.class.getName() + " <host> <port>");
      System.err.println();
      System.err.println("Eg. to test the SSL certificate at https://localhost, use");
      System.err.println("  java " + SSLPoke.class.getName() + " localhost 443");

      SSLPoke sp = new SSLPoke();

      sp.callSSL(paramArrayOfString[0], Integer.parseInt(paramArrayOfString[1]) );

    }



  }

  public void callSSL(String host, int port) {

	    try
	    {
	      SSLSocketFactory localSSLSocketFactory = (SSLSocketFactory)SSLSocketFactory.getDefault();
	      SSLSocket localSSLSocket = (SSLSocket)localSSLSocketFactory.createSocket(host, port);

	      //
	      /*SSLParameters params = new SSLParameters();
	      params.setProtocols(new String[] {"TLSv1.2"});
	      localSSLSocket.setSSLParameters(params);
		  */

	      InputStream localInputStream = localSSLSocket.getInputStream();
	      OutputStream localOutputStream = localSSLSocket.getOutputStream();

	      localOutputStream.write(1);
	      while (localInputStream.available() > 0) {
	        System.out.print(localInputStream.read());
	      }
	      System.out.println("Successfully connected");

	    }
	    catch (SSLHandshakeException localSSLHandshakeException)
	    {
	      if (localSSLHandshakeException.getCause() != null) {
	        localSSLHandshakeException.getCause().printStackTrace();
	      } else {
	        localSSLHandshakeException.printStackTrace();
	      }
	    }
	    catch (Exception localException)
	    {
	      localException.printStackTrace();
	    }

  }
}
