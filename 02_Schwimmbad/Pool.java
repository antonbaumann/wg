import java.text.DecimalFormat;
import java.util.ArrayList;

/**
 * Created by ASUS on 09.09.2017.
 */
public class Pool {

    public boolean weekend;
    public ArrayList<Integer> adults;
    public ArrayList<Integer> youths;
    public ArrayList<Integer> kids;
    public boolean holidays;
    public int credit;

    public Pool(boolean wknd, int[] prsns, boolean hldys, int crdt) {
        weekend = wknd;
        adults = new ArrayList<Integer>();
        youths = new ArrayList<Integer>();
        kids = new ArrayList<Integer>();
        for (int human : prsns) {
            if (human > 17) {
                adults.add(human);
            } else if (human > 3) {
                youths.add(human);
            } else {
                kids.add(human);
            }
        }
        holidays = hldys;
        credit = crdt;
    }

    public Pool(Pool pl) {
        weekend = pl.weekend;
        adults = new ArrayList<>(pl.adults);
        youths = new ArrayList<>(pl.youths);
        kids = new ArrayList<>(pl.kids);
        holidays = pl.holidays;
        credit = pl.credit;
    }

    public ArrayList<String> getTickets() {
        ArrayList<Integer> adults2 = new ArrayList<Integer>();
        for (int human : adults) {
            adults2.add(human);
        }
        ArrayList<Integer> youths2 = new ArrayList<Integer>();
        for (int human : youths) {
            youths2.add(human);
        }
        ArrayList<String> tickets = new ArrayList<String>();
        if (!weekend) {
            while (adults.size() + youths.size() > 5) {
                int count = 0;
                if ((adults.size() + youths.size()) % 6 > 3) {
                    while (count < 6) {
                        if (adults.size() >= youths.size()) {
                            adults.remove(0);
                            count++;
                        } else {
                            youths.remove(0);
                            count++;
                        }
                    }
                } else {
                    while (count < 6) {
                        if (!adults.isEmpty()) {
                            adults.remove(0);
                            count++;
                        } else {
                            youths.remove(0);
                            count++;
                        }
                    }
                }
                tickets.add("Tageskarte");
                //for(String ticket:tickets){
                //    System.out.println(ticket);
                //}
                //System.out.println();
            }
            if ((adults.size() > 1 && youths.size() > 1) || (!adults.isEmpty() && youths.size() > 2)) {
                int adcount = 0;
                int ycount = 0;
                while (adcount < 2 && !adults.isEmpty()) {
                    adcount++;
                    adults.remove(0);
                }
                while (ycount < 4 - adcount) {
                    ycount++;
                    youths.remove(0);
                }
                tickets.add("Familienkarte");
                //for(String ticket:tickets){
                //    System.out.println(ticket);
                //}
                //System.out.println();
            }
            if (adults.size() > 4) {
                tickets.add("Tageskarte");
                //for(String ticket:tickets){
                //    System.out.println(ticket);
                //}
                //System.out.println();
                while (!adults.isEmpty()) {
                    adults.remove(0);
                }
            }
        } else {
            while ((adults.size() > 1 && !youths.isEmpty()) || (!adults.isEmpty() && youths.size() > 1)) {
                int adcount = 0;
                int ycount = 0;
                while (adcount < 2 && !adults.isEmpty()) {
                    adcount++;
                    adults.remove(0);
                }
                while (ycount < 4 - adcount && !youths.isEmpty()) {
                    ycount++;
                    youths.remove(0);
                }
                tickets.add("Familienkarte");
                //for(String ticket:tickets){
                //    System.out.println(ticket);
                //}
                //System.out.println();
            }
        }
        for (int human : adults) {
            tickets.add("EinzelkarteErwachsener");
            //for(String ticket:tickets){
            //    System.out.println(ticket);
            //}
            //System.out.println();
        }
        for (int human : youths) {
            tickets.add("EinzelkarteJugend");
            //for(String ticket:tickets){
            //    System.out.println(ticket);
            //}
            //System.out.println();
        }
        adults = adults2;
        youths = youths2;
        return tickets;
    }

    public double getPrize() {
        ArrayList<String> tickets = this.getTickets();
        double res = 0;
        for (String ticket : tickets) {
            if (ticket.equals("Tageskarte")) {
                res += 11;
            } else if (ticket.equals("Familienkarte")) {
                res += 8;
            } else if (!weekend) {
                if (ticket.equals("EinzelkarteErwachsener")) {
                    res += 2.8;
                } else {
                    res += 2;
                }
            } else {
                if (ticket.equals("EinzelkarteErwachsener")) {
                    res += 3.5;
                } else {
                    res += 2.5;
                }
            }
        }
        return res;
    }

    public static void main(String[] args) {
        DecimalFormat df = new DecimalFormat("#.##");
        Pool test = new Pool(true, new int[]{13, 13, 13, 13, 20, 2}, true, 0);
        Pool test2 = new Pool(test);
        if (!test.kids.isEmpty()) {
            if (test.adults.isEmpty()) {
                System.out.println("Illegal kid(s) detected! Exterminate!");
                System.exit(1);
            }
        }
        if (!test.holidays) {
            while (test.credit > 1) {
                if (test.adults.size() >= test.youths.size()) {
                    test.adults.remove(0);
                } else {
                    test.youths.remove(0);
                }
                test.credit--;
            }
        }
        if (test.credit == 1 && !test.holidays) {
            if (test2.adults.size() >= test2.youths.size()) {
                test2.adults.remove(0);
            } else {
                test2.youths.remove(0);
            }
            test.credit--;
            if (test.getPrize() * 0.9 < test2.getPrize()) {
                System.out.print("Preis: ");
                System.out.println(df.format(test.getPrize() * 0.9));
                System.out.print("Tickets: ");
                for (String ticket : test.getTickets()) {
                    System.out.print(ticket + ", ");
                }
            } else {
                System.out.print("Preis: ");
                System.out.println(df.format(test2.getPrize()));
                System.out.print("Tickets: ");
                for (String ticket : test2.getTickets()) {
                    System.out.print(ticket + ", ");
                }
            }
        } else {
            System.out.print("Preis: ");
            System.out.println(df.format(test.getPrize()));
            System.out.print("Tickets: ");
            for (String ticket : test.getTickets()) {
                System.out.print(ticket + ", ");
            }
        }
    }
}