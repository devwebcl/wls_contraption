package cl.devweb.btrace;

//import all BTrace annotations
import com.sun.btrace.annotations.*;
//import statics from BTraceUtils class
import static com.sun.btrace.BTraceUtils.*;

//@BTrace annotation tells that this is a BTrace program
@BTrace
public class HelloWorld {

 // @OnMethod annotation tells where to probe.
 // In this example, we are interested in entry 
 // into the Thread.start() method. 
 @OnMethod(
     clazz="java.lang.Thread",
     method="start"
 )
 public static void func() {
     // println is defined in BTraceUtils
     // you can only call the static methods of BTraceUtils
     println("about to start a thread!");
 }

}


