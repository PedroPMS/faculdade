import java.io.*;
import java.util.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;

class DividirArquivo {
    BufferedReader reader;
    PrintWriter writer;
    double bytesArquivo;
    String nomeArquivo;
    int tamanhoBuffer;
    ArrayList<String> listaArquivos = new ArrayList<String>();

    public DividirArquivo(String nomeArquivo) {
        this.nomeArquivo = nomeArquivo;
        try {
            this.reader = new BufferedReader(new FileReader(nomeArquivo));
        } catch (Exception e) {
            e.printStackTrace();
        }

        Path path = Paths.get(nomeArquivo);

        try {
            this.bytesArquivo = Files.size(path);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void dividirArquivo() {

        double memoriaMaxima = 1000000;
        double tamanhoObjetoAgenda = 100;

        DividirArquivo entrada = new DividirArquivo(this.nomeArquivo);
        int numeroDeLinhas = entrada.getNumeroDeLinha();

        double tamanhoTotal = tamanhoObjetoAgenda * numeroDeLinhas;
        double numeroArquivos = Math.floor(tamanhoTotal / memoriaMaxima);
        if (numeroArquivos < 1) {
            numeroArquivos = 1;
        }

        this.tamanhoBuffer = (int) Math.ceil(numeroDeLinhas / numeroArquivos);

        Source fonte = new Source(this.nomeArquivo, false);
        Buffer buffer = new Buffer(this.tamanhoBuffer, fonte);

        int arquivo = 1;
        for (int i = 0; i < numeroArquivos; i++) {
            String nomeArquivoNovo = "arq" + arquivo + ".csv";
            Source saida = new Source(nomeArquivoNovo, true);
            this.listaArquivos.add(nomeArquivoNovo);
            buffer.criarNovoArquivo(saida);
            arquivo = arquivo + 1;
        }
    }

    public void apagarArquivosTemporarios() {
        for (int i = 0; i < this.listaArquivos.size(); i++) {
            String arquivo = this.listaArquivos.get(i);
            File file = new File(arquivo);
            file.delete();
        }
    }

    private int getNumeroDeLinha() {
        String input = null;
        int count = 0;

        try {
            input = this.reader.readLine();
        } catch (Exception e) {
            e.printStackTrace();
        }

        while (input != null) {
            count++;
            try {
                input = this.reader.readLine();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return count;
    }
}