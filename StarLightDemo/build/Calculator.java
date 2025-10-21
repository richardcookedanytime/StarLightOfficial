public class Calculator {

    public static void main(String[] args) {
        Object x = 10;
        Object y = 5;
        Object sum = add(x, y);
        Object product = multiply(x, y);
        System.out.println(("Sum: " + sum));
        System.out.println(("Product: " + product));
    }

    public static int add(Object a, Object b) {
        return (((Integer) a) + ((Integer) b));
    }

    public static int multiply(Object a, Object b) {
        return (((Integer) a) * ((Integer) b));
    }

}