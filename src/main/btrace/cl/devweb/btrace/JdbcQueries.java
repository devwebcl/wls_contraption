package cl.devweb.btrace;

import static com.sun.btrace.BTraceUtils.*;
import java.sql.Statement;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;
import com.sun.btrace.*;
import com.sun.btrace.annotations.*;
/**
 * BTrace script to print timings for all executed JDBC statements on an event.
 * <p>
 *
 * https://blogs.oracle.com/sundararajan/btrace-in-the-real-world
 * https://visualvm.github.io/plugins.html
 *
 * @author Chris Glencross
 */


@BTrace
public class JdbcQueries {
    private static Map preparedStatementDescriptions = newWeakMap();
    private static Map statementDurations = newHashMap();
    // VERBOSE: @TLS makes the field "thread local" -- sort of like using java.lang.ThreadLocal
    @TLS
    private static String preparingStatement;
    @TLS
    private static long timeStampNanos;
    @TLS
    private static String executingStatement;
    /**
     * If "--stack" is passed on command line, print the Java stack trace of the JDBC statement.
     *
     * VERBOSE: Command line arguments to BTrace are accessed as $(N) where N is the command line arg position.
     * 
     * Otherwise we print the SQL.
     */
    private static boolean useStackTrace = $(2) != null && strcmp("--stack", $(2)) == 0;
    // The first couple of probes capture whenever prepared statement and callable statements are
    // instantiated, in order to let us track what SQL they contain.
    /**
     * Capture SQL used to create prepared statements.
     *
     * VERBOSE: +foo in clazz means foo and it's subtypes. Note the use of regular expression
     * for method names. With that BTrace matches all methods starting with "prepare". The
     * type "AnyType" matches any Java type.
     * 
     * @param args - the list of method parameters. args[1] is the SQL.
     */
    @OnMethod(clazz = "+java.sql.Connection", method = "/prepare.*/")
    public static void onPrepare(AnyType[] args) {
        preparingStatement = useStackTrace ? jstackStr() : str(args[1]);
    }
    /**
     * Cache SQL associated with a prepared statement.
     *
     * VERBOSE: By default, @OnMethod matches method entry points. Modifying with @Location 
     * annotation to match the method return points.
     * 
     * @param arg - the return value from the prepareXxx() method.
     */
    @OnMethod(clazz = "+java.sql.Connection", method = "/prepare.*/", location = @Location(Kind.RETURN))
    public static void onPrepareReturn(AnyType arg) {
        if (preparingStatement != null) {
            print("P"); // Debug Prepared
            Statement preparedStatement = (Statement) arg;
            put(preparedStatementDescriptions, preparedStatement, preparingStatement);
            preparingStatement = null;
        }
    }
    // The next couple of probes intercept the execution of a statement. If it execute with no-args,
    // then it must be a prepared statement or callable statement. Get the SQL from the probes up above.
    // Otherwise the SQL is in the first argument.
    @OnMethod(clazz = "+java.sql.Statement", method = "/execute.*/")
    public static void onExecute(AnyType[] args) {
        timeStampNanos = timeNanos();
        if (args.length == 1) {
            // No SQL argument; lookup the SQL from the prepared statement
            Statement currentStatement = (Statement) args[0]; // this
            executingStatement = get(preparedStatementDescriptions, currentStatement);
        } else {
            // Direct SQL in the first argument
            executingStatement = useStackTrace ? jstackStr() : str(args[1]);
        }
    }
    @OnMethod(clazz = "+java.sql.Statement", method = "/execute.*/", location = @Location(Kind.RETURN))
    public static void onExecuteReturn() {
        if (executingStatement == null) {
            return;
        }
        print("X"); // Debug Executed
        long durationMicros = (timeNanos() - timeStampNanos) / 1000;
        AtomicLong ai = get(statementDurations, executingStatement);
        if (ai == null) {
            ai = newAtomicLong(durationMicros);
            put(statementDurations, executingStatement, ai);
        } else {
            addAndGet(ai, durationMicros);
        }
        executingStatement = null;
    }
    // VERBOSE: @OnEvent probe fires whenever BTrace client sends "event" command.
    // The command line BTrace client sends BTrace events when user pressed Ctrl-C 
    // (more precisely, on receiving SIGINT signal)
    @OnEvent
    public static void onEvent() {
        println("---------------------------------------------");
        printNumberMap("JDBC statement executions / microseconds:", statementDurations);
        println("---------------------------------------------");
    }
}
 
