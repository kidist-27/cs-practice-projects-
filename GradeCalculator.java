
import java.util.Scanner;

public class GradeCalculator {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("=== Student Grade Calculator ===");

        double javaMark = readMark(scanner, "Java");
        double networkingMark = readMark(scanner, "Networking");
        double databaseMark = readMark(scanner, "Database");

        double average = (javaMark + networkingMark + databaseMark) / 3.0;

        String grade = calculateGrade(average);

        System.out.printf("%nAverage: %.2f%n", average);
        System.out.println("Grade: " + grade);

        scanner.close();
    }

    private static double readMark(Scanner scanner, String subject) {
        while (true) {
            System.out.print("Enter " + subject + " mark (0-100): ");

            if (scanner.hasNextDouble()) {
                double mark = scanner.nextDouble();

                if (mark >= 0 && mark <= 100) {
                    return mark;
                }

                System.out.println("Mark must be between 0 and 100.");
            } else {
                System.out.println("Please enter a valid number.");
                scanner.next();
            }
        }
    }

    private static String calculateGrade(double average) {
        if (average >= 90) return "A";
        if (average >= 80) return "B";
        if (average >= 70) return "C";
        if (average >= 60) return "D";
        return "F";
    }
}
