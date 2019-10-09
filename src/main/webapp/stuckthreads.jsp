<%-- 
    Document   : index
    Created on : 04.04.2012, 10:59:14
    Author     : frank
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>StuckThreadsForFree!</title>
    </head>
    <body>
        <h1>StuckThreadForFree</h1>
        <FORM NAME="data" METHOD="POST" Action="/wls-contraption/stuck">

            Number of threads to run <INPUT TYPE="TEXT"   NAME="numberOfThreads" VALUE="3"><br/>
            Seconds to keep threads busy <INPUT TYPE="TEXT"   NAME="timeBusy" VALUE="700"><br/>
            <p/>

            <p><b>Choose a way make them stuck:</b><br>
                <input type="RADIO" value="calc" name="select" id="navRadio01" >
                <label for="navRadio01">Calculating sin()</label><br>
                <input type="RADIO" value="sleep"    name="select" id="navRadio02" checked="checked">
                <label for="navRadio02">Thread.sleep()</label><br>
            <p/>
            <INPUT TYPE="SUBMIT" NAME="go" VALUE="submit">
        </FORM>
</body>
</html>
