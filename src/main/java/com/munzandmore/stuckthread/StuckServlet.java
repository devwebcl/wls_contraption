package com.munzandmore.stuckthread;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Date;
import javax.ejb.EJB;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * http://www.munzandmore.com/2012/ora/weblogic-stuck-threads-howto
 *
 * @author frank
 */
@WebServlet(urlPatterns = "/stuck")
public class StuckServlet extends HttpServlet {

    /**
     * 
     */
    private static final long serialVersionUID = 1L;
    /**
     * Processes requests for both HTTP
     * <code>GET</code> and
     * <code>POST</code> methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @EJB
    private LongRunningEJB lr;

    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        int numberOfThreads = Integer.parseInt(request.getParameter("numberOfThreads"));
        int timeBusy = Integer.parseInt(request.getParameter("timeBusy"));
        String select = request.getParameter("select");
        
        
        PrintWriter out = response.getWriter();
        try {
        
            out.println("<html>");
            out.println("<head>");
            out.println("<title>Servlet stuck</title>");
            out.println("</head>");
            out.println("<body>");
            out.println("<h1>Servlet to create stuck threads called... </h1>");


            for (int i = 0; i < numberOfThreads; i++) {
               
                        
                if ("calc".equals(select)) {
                    out.println("asynchronously calling EJB method calc("+timeBusy+" sec) in iteration " + i + " at " + new Date() + "</br>");
                    lr.threadCalc(timeBusy);
                } else if ("sleep".equals(select)) {
                    out.println("asynchronously calling EJB method sleep("+timeBusy+" sec) in iteration " + i + " at " + new Date() + "</br>");
                lr.threadSleep(timeBusy);
                } else throw new IllegalArgumentException("no vaild select for thread blocking");
            }

            out.println("</body>");
            out.println("</html>");
        } finally {
            out.close();
        }
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP
     * <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Handles the HTTP
     * <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }
}
