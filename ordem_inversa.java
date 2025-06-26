import java.util.*;
class Main {
    public static void main(String[] args) {
        int x[] = new int[5];
        int i;
        Scanner sc = new Scanner(System.in);
        System.out.println("Insira 5 numeros: ");
        for(i = 0; i < 5; i++) {
            x[i] = sc.nextInt();
        }
        System.out.println("Exibir os numeros em ordem inversa:");
        for(i = 4; i >= 0; i--) {
            System.out.println(x[i]);
        }
        sc.close();
    }
}
