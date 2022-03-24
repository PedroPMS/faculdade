import java.util.*;

public class KWay {
    public static void main(String[] args) {
        long time1 = System.currentTimeMillis();

        DividirArquivo entrada = new DividirArquivo("Entrada4M.csv");
        entrada.dividirArquivo();

        ArrayList<Buffer> buffers = new ArrayList<Buffer>();

        for (int i = 0; i < entrada.listaArquivos.size(); i++) {
            String arquivo = entrada.listaArquivos.get(i);

            Source fonte = new Source(arquivo, false);
            Buffer buffer = new Buffer(entrada.tamanhoBuffer, fonte);
            buffers.add(buffer);
        }

        Source saida = new Source("saida-kway4m.csv", true); // saida dos dados
        Buffer bufferSaida = new Buffer(0, saida); // buffer usado para intermediar a escrita

        Merging merging = new Merging();
        merging.mergeBuffers(buffers, bufferSaida);

        // Fecha o buffer de saída
        bufferSaida.closeOutputBuffer();
        entrada.apagarArquivosTemporarios();

        long time2 = System.currentTimeMillis();
        System.out.println("Tempo K-Way Merge " + (time2 - time1) + "ms");
    }
}
