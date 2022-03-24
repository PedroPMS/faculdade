import java.util.*;

public class Buffer {
    public int tamanhoBuffer;
    private int i;
    private ArrayList<Agenda> bufferAgenda = new ArrayList<Agenda>();
    private Source source;

    public Buffer(int tamanhoBuffer, Source source) {
        this.source = source;
        this.tamanhoBuffer = tamanhoBuffer;
        this.i = tamanhoBuffer;
    }

    public Agenda getCurrent() {
        if (this.i != this.tamanhoBuffer) { // quando o buffer está vazio carrega da fonte original
            return this.bufferAgenda.get(this.i - 1);
        }
        return null;
    }

    public Agenda read() {
        if (this.i == this.tamanhoBuffer) { // quando o buffer está vazio carrega da fonte original
            this.load();
            this.i = 0;
        }

        return this.bufferAgenda.get(this.i++);
    }

    public void criarNovoArquivo(Source saida) {
        ArrayList<String> lista = new ArrayList<String>();
        for (i = 0; i < this.tamanhoBuffer; i++) {
            String linha = this.source.read();
            if (linha == null) {
                continue;
            }
            lista.add(linha);
        }

        Collections.sort(lista);
        for (i = 0; i < lista.size(); i++) {
            String linha = lista.get(i);
            saida.write(linha);
        }
        saida.closeOutputBuffer();
    }

    public int load() {
        for (i = 0; i < this.tamanhoBuffer; i++) {
            String linha = this.source.read();
            if (linha == null) { // se não tiver elementos para ler
                this.bufferAgenda.add(i, null); // adiciona null no buffer
                continue; // avança para próxima iteração do loop
            }

            String[] valores = linha.split(",");

            String nomeCompleto = valores[0];
            String telefone = valores[1];
            String cidade = valores[2];
            String pais = valores[3];

            Agenda pessoaAgenda = new Agenda(nomeCompleto, telefone, cidade, pais);
            this.bufferAgenda.add(i, pessoaAgenda);
        }

        return 0;
    }

    public void print() {
        System.out.println(bufferAgenda);
    }

    public void write(Agenda agenda) {
        String linhaCsv = agenda.getNomeCompleto() + ',' + agenda.getTelefone() + ',' + agenda.getCidade() + ','
                + agenda.getPais();

        this.source.write(linhaCsv);
    }

    public void closeOutputBuffer() {
        this.source.closeOutputBuffer();
    }
}
