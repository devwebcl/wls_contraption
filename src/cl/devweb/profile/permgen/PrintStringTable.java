package cl.devweb.profile.permgen;

import sun.jvm.hotspot.memory.StringTable;
import sun.jvm.hotspot.memory.SystemDictionary;
import sun.jvm.hotspot.oops.Instance;
import sun.jvm.hotspot.oops.InstanceKlass;
import sun.jvm.hotspot.oops.OopField;
import sun.jvm.hotspot.oops.TypeArray;
import sun.jvm.hotspot.runtime.VM;
import sun.jvm.hotspot.tools.Tool;
/**
 * https://github.com/puneetlakhina/javautils/blob/master/src/com/blogspot/sahyog/PrintStringTable.java
 *
 *
 * Print the string literal pool of a running JVM.
 * Based on http://www.docjar.com/html/api/sun/jvm/hotspot/tools/PermStat.java.html
 * Usage: java com.blogspot.sahyog.PrintStringTable &lt;Running JVM's PID&gt; <br />
 * You need to add sa-jdi.jar to your class path. This is generally available in your JDK's lib directory. Also, you might need to run this class with super user privileges in order to access the other JVM.
 * @author puneet
 *
 */
public class PrintStringTable extends Tool {
    public PrintStringTable() {

    }
    class StringPrinter implements StringTable.StringVisitor {
        private final OopField stringValueField;
        public StringPrinter() {
            InstanceKlass strKlass = SystemDictionary.getStringKlass();
            stringValueField = (OopField) strKlass.findField("value", "[C");
        }
        @Override
        public void visit(Instance instance) {
            TypeArray charArray = ((TypeArray)stringValueField.getValue(instance));
            StringBuilder sb = new StringBuilder();
            for(long i=0;i<charArray.getLength();i++) {
                sb.append(charArray.getCharAt(i));
            }
            System.out.println("Address: " + instance.getHandle() + " Content: " + sb.toString());
        }

    }
    public static void main(String args[]) throws Exception {
        /*if(args.length == 0 || args.length > 1) {
        System.err.println("Usage: java com.blogspot.sahyog.PrintStringTable <PID of the JVM whose string table you want to print>");
        System.exit(1);
        }*/
        String [] args2 = { "58378" }; // PID, obviamente es
        PrintStringTable pst = new PrintStringTable();
        pst.start(args2);
        pst.stop();
    }

    @Override
    public void run() {
        StringTable table = VM.getVM().getStringTable();
        table.stringsDo(new StringPrinter());
    }
}
