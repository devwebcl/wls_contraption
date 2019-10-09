package com.munzandmore.stuckthread;


import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.Asynchronous;
import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;

/**
 *
 * @author frank
 */
@Stateless
@Asynchronous
public class LongRunningEJB {

    @TransactionAttribute(TransactionAttributeType.NOT_SUPPORTED)
    public void threadSleep(int seconds) {
        try {
            Thread.sleep(seconds * 1000);
        } catch (InterruptedException ex) {
            Logger.getLogger(LongRunningEJB.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    @TransactionAttribute(TransactionAttributeType.NOT_SUPPORTED)
    public void threadCalc(int seconds) {

        double start = 0;
        long t0 = System.currentTimeMillis();

        while (((System.currentTimeMillis() - t0) / 1000) < seconds) {
            double x = Math.sin(start++);
        }

    }
}
