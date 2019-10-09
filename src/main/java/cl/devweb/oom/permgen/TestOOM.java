package cl.devweb.oom.permgen;

public class TestOOM {

    public static void main(String[] args) throws Exception {
        //new HeapOOM().oomByMem();

    }

    public static void showMemoryInfo()	{

        System.out.print("\nTotal memory : " + Runtime.getRuntime().totalMemory());

        System.out.print(" Free : " + Runtime.getRuntime().freeMemory());

        System.out.print(" Max : " + Runtime.getRuntime().maxMemory());

    }

}
