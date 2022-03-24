import java.io.*;
import java.util.*;

public class Externo {
    static final int bufblocks = 64;

    public static String[] FName = new String[4];

    public static int IN1 = 0;
    public static int IN2 = 1;
    public static int OUT1 = 2;
    public static int OUT2 = 3;

    ////// Code for Quicksort ////////////////////////////////////
    static void swap(ArrayList<String> array, int p1, int p2) {
        Collections.swap(array, p1, p2);
    }

    static int partition(ArrayList<String> array, int l, int r, String pivot) {
        do { // Move the bounds inward until they meet
            while (array.get(++l).compareTo(pivot) < 0)
                ; // Move left bound right
            while ((r != 0) && (array.get(--r).compareTo(pivot) > 0))
                ; // Move right bound
            swap(array, l, r); // Swap out-of-place values
        } while (l < r); // Stop when they cross
        swap(array, l, r); // Reverse last, wasted swap
        return l; // Return first position in right partition
    }

    static void qsort(ArrayList<String> array, int i, int j) { // Quicksort
        int pivotindex = (i + j) / 2;
        swap(array, pivotindex, j); // Stick pivot at end
        int k = partition(array, i - 1, j, array.get(j));
        swap(array, k, j); // Put pivot in place
        if ((k - i) > 1)
            qsort(array, i, k - 1); // Sort left partition
        if ((j - k) > 1)
            qsort(array, k + 1, j); // Sort right partition
    }
    ////// Fim Quicksort ////////////////////////////////

    // Quicksort é usado para gerar os primeiros 2 arquivos de entrada
    static void primeiraPassagem(BufferedReader in, PrintWriter out1, PrintWriter out2, int numeroDeLinhas)
            throws IOException {
        int bufrecs = bufblocks;
        ArrayList<String> buffer = new ArrayList<String>();
        int runs = numeroDeLinhas / bufrecs;
        PrintWriter temp;

        for (int i = 0; i < runs; i++) {
            for (int j = 0; j < bufrecs; j++) {
                String linha = in.readLine();
                buffer.add(j, linha);
            }
            qsort(buffer, 0, bufrecs - 1);
            for (int j = 0; j < bufrecs; j++) {
                out1.println(buffer.get(j));
            }
            temp = out1;
            out1 = out2;
            out2 = temp;
        }
    }

    // 2-Way Merge
    static void passagem2Way(BufferedReader in1, BufferedReader in2, PrintWriter out1, PrintWriter out2, int numruns,
            int runlen) throws IOException {
        PrintWriter temp;
        String val1, val2;
        int in1cnt, in2cnt;
        int outcnt;

        for (int i = 0; i < numruns; i++) {
            val1 = in1.readLine();
            val2 = in2.readLine();
            // System.out.println("1" + val1 + " ----- " + val2);
            in1cnt = 1;
            in2cnt = 1;
            outcnt = 0;
            while (outcnt < 2 * runlen) {
                if (val1 == null || val1.compareTo(val2) <= 0) {
                    out1.println(val1);
                    outcnt++;
                    if (in1cnt < runlen) {
                        val1 = in1.readLine();
                        in1cnt++;
                    } else {
                        out1.println(val2);
                        outcnt++;
                        while (in2cnt < runlen) {
                            val2 = in2.readLine();
                            in2cnt++;
                            out1.println(val2);
                            outcnt++;
                        }
                    }
                } else {
                    out1.println(val2);
                    outcnt++;
                    if (in2cnt < runlen) {
                        val2 = in2.readLine();
                        in2cnt++;
                    } else {
                        out1.println(val1);
                        outcnt++;
                        while (in1cnt < runlen) {
                            val1 = in1.readLine();
                            in1cnt++;
                            out1.println(val1);
                            outcnt++;
                        }
                    }
                }
            }
            temp = out1;
            out1 = out2;
            out2 = temp;
        }
    }

    // Do an external sort
    static void exmergesort(String arquivoEntrada, String arquivoSaida, int numeroDeLinhas) throws IOException {
        int temp;

        BufferedReader in = new BufferedReader(new FileReader(arquivoEntrada));
        PrintWriter out1 = new PrintWriter(new FileOutputStream(new File(FName[IN1])));
        PrintWriter out2 = new PrintWriter(new FileOutputStream(new File(FName[IN2])));
        primeiraPassagem(in, out1, out2, numeroDeLinhas);
        in.close();
        out1.close();
        out2.close();

        // Série de 2-way merge para ordenar os arquivos
        int numRuns = numeroDeLinhas / bufblocks;
        for (int i = numRuns; i > 2; i /= 2) {
            BufferedReader in1 = new BufferedReader(new FileReader(FName[IN1]));
            BufferedReader in2 = new BufferedReader(new FileReader(FName[IN2]));
            out1 = new PrintWriter(new FileOutputStream(new File(FName[OUT1])));
            out2 = new PrintWriter(new FileOutputStream(new File(FName[OUT2])));
            passagem2Way(in1, in2, out1, out2, i / 2, numeroDeLinhas / i);
            in1.close();
            in2.close();
            out1.close();
            out2.close();
            temp = IN1;
            IN1 = OUT1;
            OUT1 = temp;
            temp = IN2;
            IN2 = OUT2;
            OUT2 = temp;
        }

        // Junta os 2 arquivos finais no arquivo de saída
        if (numRuns > 1) {
            BufferedReader in1 = new BufferedReader(new FileReader(FName[IN1]));
            BufferedReader in2 = new BufferedReader(new FileReader(FName[IN2]));
            out1 = new PrintWriter(new FileOutputStream(new File(arquivoSaida)));
            passagem2Way(in1, in2, out1, null, 1, numeroDeLinhas / 2);
            in1.close();
            in2.close();
            out1.close();
        }
    }

    // Main routine for external sort
    public static void main(String args[]) throws IOException {

        String nomeArquivo = "Entrada4M.csv";
        String nomeArquivoOut = "saida-externo4m.csv";

        int numeroDeLinhas = getNumeroDeLinha(nomeArquivo);
        FName[IN1] = "input1.txt";
        FName[IN2] = "input2.txt";
        FName[OUT1] = "out1.txt";
        FName[OUT2] = "out2.txt";

        File f = new File(FName[IN1]);
        if (f.exists())
            f.delete();
        f = new File(FName[IN2]);
        if (f.exists())
            f.delete();
        f = new File(FName[OUT1]);
        if (f.exists())
            f.delete();
        f = new File(FName[OUT2]);
        if (f.exists())
            f.delete();

        long time1 = System.currentTimeMillis();
        exmergesort(nomeArquivo, nomeArquivoOut, numeroDeLinhas);
        long time2 = System.currentTimeMillis();
        System.out.println("Tempo Merge Sort Externo " + (time2 - time1) + "ms");
    }

    static int getNumeroDeLinha(String nomeArquivo) {
        BufferedReader entrada;
        String input = null;
        int count = 0;

        try {
            entrada = new BufferedReader(new FileReader(nomeArquivo));
            input = entrada.readLine();

            while (input != null) {
                count++;
                try {
                    input = entrada.readLine();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            entrada.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return count;
    }

}
