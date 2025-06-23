import java.util.LinkedHashSet;
public class RemoveDuplicate {
    public static void main(String[] args) {
        String str = "Programando";
        char[] ch = str.toCharArray();

        LinkedHashSet<Character> set = new LinkedHashSet<>();
        for (char c : ch) {
            set.add(c);
        }

        // Monta a string sem duplicatas
        StringBuilder sb = new StringBuilder();
        for (char c : set) {
            sb.append(c);
        }

        System.out.println("String sem duplicatas: " + sb.toString());
    }
};
