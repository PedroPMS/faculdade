public class Agenda {
    private String nomeCompleto, telefone, cidade, pais;

    public Agenda(String nomeCompleto, String telefone, String cidade, String pais) {
        this.nomeCompleto = nomeCompleto;
        this.telefone = telefone;
        this.cidade = cidade;
        this.pais = pais;
    }

    public String getNomeCompleto() {
        return this.nomeCompleto;
    }

    public String getTelefone() {
        return this.telefone;
    }

    public String getCidade() {
        return this.cidade;
    }

    public String getPais() {
        return this.pais;
    }

    public int getTamanho() {
        int tamanhoObjetoEmBytes = 0;
        try {
            tamanhoObjetoEmBytes = this.nomeCompleto.getBytes("UTF-8").length + this.telefone.getBytes("UTF-8").length
                    + this.cidade.getBytes("UTF-8").length + this.pais.getBytes("UTF-8").length + 16;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return tamanhoObjetoEmBytes;
    }
}
