import java.io.*;

class Source {
    BufferedReader reader;
    PrintWriter writer;

    public Source(String nomeArquivo, boolean isEscrita) {
        try {
            // Inicia o buffer para escrita ou leitura dependendo da variável isEscrita
            if (isEscrita) {
                this.writer = new PrintWriter(new FileOutputStream(new File(nomeArquivo), true));
            } else {
                this.reader = new BufferedReader(new FileReader(nomeArquivo));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Lê a próxima linha do arquivo
    public String read() {
        if (this.reader == null) {
            return null;
        }

        try {
            String linha = this.reader.readLine();
            if (linha != null) {
                return linha;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }

    public void write(String conteudo) {
        if (this.writer == null) {
            return;
        }

        this.writer.println(conteudo);
    }

    public void closeOutputBuffer() {
        if (writer == null) {
            return;
        }

        this.writer.close();
    }
}