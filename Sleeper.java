public class Sleeper {
    public static void main(String[] args) {
        try {
            // Sleep for 2000 milliseconds (2 seconds)
            Thread.sleep(60000);
        } catch (InterruptedException e) {
            // Handle interrupted exception
            e.printStackTrace();
        }
    }
}
