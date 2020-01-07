package cl.devweb.oom.heap;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;
import java.util.logging.Logger;


public class StaticOOM {

    public List<Integer> list = new ArrayList<>();
    
    public void populateList() {
        
    	Logger.getGlobal().info("Debug Point 2");
    	System.out.println("Debug Point 2");
 
        for (int i = 0; i < 10000000; i++) {
            list.add(new Random().nextInt());
        }
        Logger.getGlobal().info("Debug Point 3");
        System.out.println("Debug Point 3");
        
    }
    
    
    public static void main(String[] args) {
    	
    	Scanner keyboard = new Scanner(System.in);
    	
        Logger.getGlobal().info("Debug Point 1");
        System.out.println("Debug Point 1");
        
        new StaticOOM().populateList();

        Logger.getGlobal().info("Debug Point 4");
        System.out.println("Debug Point 4");
        
        try {
            
        	System.gc();
            Thread.sleep(5000);
            
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

}


