
/* compile with additional options for jdk 6: -target 6 
 * or run in python with absolute path to the java like: 
 *     javart = 'c:/ProgramData/Oracle/Java/javapath/java'
 *     subprocess.check_output([javart, '-jar', 'qtclick.jar', x, y, n])
 */

import java.awt.AWTException;
import java.awt.Robot;
import java.awt.event.InputEvent;

public class TestQtClick {
    public static void main(String[] args){
        int x = 0, y = 0, n = 0;
        if ( args.length == 3 ) {
            x = Integer.parseInt(args[0]);
            y = Integer.parseInt(args[1]);
            n = Integer.parseInt(args[2]); /* reference */
        } else {
            System.out.println("java error args size not 3");
            return;
        }
        System.out.println(String.format("java input %d %d %d", x, y, n));
        Robot bot;
        try {
            bot = new Robot();
            int mask = InputEvent.BUTTON1_DOWN_MASK;
            bot.mouseMove(x, y);
            bot.mousePress(mask);
            bot.mouseRelease(mask);
            System.out.println(String.format("java clicked %d %d %d", x, y, n));
        } catch (AWTException ex) {
            System.out.println(String.format("java error click %d %d %d",x,y,n));
        }
    }
}


