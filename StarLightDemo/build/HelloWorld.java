public class HelloWorld {

    public static void main(String[] args) {
        Object message = greet("World");
        System.out.println(message);
    }

    public static String greet(Object name) {
        return (("Hello, " + name) + "! Welcome to Starlight!");
    }

}