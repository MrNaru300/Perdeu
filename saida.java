import java.util.Random;

public class Aleatorio {
    public static boolean isFim(String s) {
        return (s.length() == 3 && s.charAt(0) == 'F' && s.charAt(1) == 'I' && s.charAt(2) == 'M');
    }

    public static void main(String[] args) {
        String linha = MyIO.readLine();
        String result = "";
        char key, repl;
        Random random = new Random(4);

        
        while (!isFim(linha)) {
            
            key = (char)('a' + (Math.abs(random.nextInt()) % 26));
            repl = (char)('a' + (Math.abs(random.nextInt()) % 26));
            for (int i = 0; i < linha.length(); i++) {
                if (linha.charAt(i) == key) result += repl;
                else result += linha.charAt(i);
            }

            MyIO.println(result);

            linha = MyIO.readLine();
            result = "";
        }
    }    
}