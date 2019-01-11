package cl.devweb.btrace; 

/* BTrace Script Template */

import com.sun.btrace.*;
import com.sun.btrace.annotations.*;
import static com.sun.btrace.BTraceUtils.*;
import static com.sun.btrace.BTraceUtils.Threads.jstackAll;


// https://dzone.com/articles/btrace-hidden-gem-java

// more info:
// https://www.zcfy.cc/original/btrace-wiki-userguide-mdash-project-kenai

@BTrace
public class TracingScript {
    @TLS private static String method;

    @OnMethod(
        clazz = "+cl.test.presentacion.controller.HomeController", 
        method = "/.*/"
    )
    // name follow onXxxx
    public static void onHome( 
            @ProbeClassName String className, 
            @ProbeMethodName String probeMethod, 
            AnyType[] args ) {
        method = strcat( strcat( className, "::" ), probeMethod );
    }
    
    @OnMethod(
        clazz = "+cl.test.presentacion.controller.HomeController", 
        method = "/.*/", 
        location = @Location( Kind.RETURN ) 
    )
    // name follow onXxxx
    public static void onHomeReturn( @Duration long duration ) {
    	
    	 //jstackAll();
    	 
         println( strcat( strcat( strcat( strcat( "Method ", method ), 
            " executed in " ), str( duration / 1_000_000 ) ), "ms" ) ); //nanoseconds --> milliseconds
    }
}


