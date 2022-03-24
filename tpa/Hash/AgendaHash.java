import java.util.*;
import java.io.*;

public class AgendaHash {
    private String nomeArquivo;
    private String primeiroContato;
    private HashTable<String, Agenda> agenda;

    AgendaHash(int tamanhoAgenda) {
        this.agenda = new HashTable<>(tamanhoAgenda);
    }

    public void menu() {

        Scanner menu = new Scanner(System.in);

        int opcao = 0;
        do {
            System.out.print("\n\n");
            System.out.print("##--Teste Estrutura de Menu--##\n\n");
            System.out.print("|-----------------------------|\n");
            System.out.print("| Opção 1 - Carregar Arquivo  |\n");
            System.out.print("| Opção 2 - Localizar Contato |\n");
            System.out.print("| Opção 3 - Inserir Contato   |\n");
            System.out.print("| Opção 4 - Excluir Contato   |\n");
            System.out.print("| Opção 5 - Atualizar Contato |\n");
            System.out.print("| Opção 6 - Salvar Dados      |\n");
            System.out.print("| Opção 7 - Fim do Programa   |\n");
            System.out.print("|-----------------------------|\n");
            System.out.print("Digite uma opção: ");

            opcao = menu.nextInt();
            switch (opcao) {
                case 1:
                    long time1 = System.currentTimeMillis();
                    System.out.println("\nOpção Carregar Arquivo Selecionada");
                    System.out.println("\nInforme o nome do arquivo: ");
                    String nomeArquivo = menu.next();
                    this.carregarArquivo(nomeArquivo);
                    long time2 = System.currentTimeMillis();
                    System.out.println("\n\nTempo Carregar Arquivo " + (time2 - time1) + "ms");
                    break;

                case 2:
                    time1 = System.currentTimeMillis();
                    menu.nextLine();
                    System.out.println("\nOpção Localizar Contato Selecionada\n");
                    System.out.println("\nInforme o nome do contato: ");
                    String nome = menu.nextLine();
                    this.localizarContato(nome);
                    time2 = System.currentTimeMillis();
                    System.out.println("\n\nTempo Localizar Contato " + (time2 - time1) + "ms");
                    break;

                case 3:
                    System.out.println("\nOpção Inserir Contato Selecionada\n");
                    System.out.println("\nInforme o nome do contato: ");
                    String nomeContato = "Pedro"; // menu.next();
                    System.out.println("\nInforme o telefone do contato: ");
                    String telefoneContato = "99999-8888"; // menu.next();
                    System.out.println("\nInforme a cidade do contato: ");
                    String cidadeContato = "Vix"; // menu.next();
                    System.out.println("\nInforme o país do contato: ");
                    String paisContato = "Brasil"; // menu.next();
                    this.inserirContato(nomeContato, telefoneContato, cidadeContato,
                            paisContato);
                    break;

                case 4:
                    System.out.println("\nOpção Excluir Contato Selecionada\n");
                    System.out.println("\nInforme o nome do contato: ");
                    String nomeExcluir = "Eugene Lueilwitz"; // menu.next();
                    this.excluirContato(nomeExcluir);
                    break;

                case 5:
                    System.out.println("\nOpção Atualizar Contato Selecionada\n");
                    System.out.println("\nInforme o nome do contato: ");
                    String nomeAtualizar = "Herbert Gutkowski"; // menu.next();
                    this.atualizarContato(nomeAtualizar, menu);
                    break;

                case 6:
                    time1 = System.currentTimeMillis();
                    System.out.println("\nOpção Salvar Contatos Selecionada\n");
                    this.salvarArquivo();
                    time2 = System.currentTimeMillis();
                    System.out.println("\n\nTempo Salvar Arquivo " + (time2 - time1) + "ms");
                    break;

                default:
                    System.out.println("\nOpção Inválida!");
                    break;

                case 7:
                    System.out.println("\nAté logo!");
                    menu.close();
            }

        } while (opcao != 7);
    }

    private void atualizarContato(String nome, Scanner menu) {
        System.out.print("\nInforme o nome atualizado do contato: ");
        String nomeAtualizado = "Herbert Silva"; // menu.next();
        System.out.print("\nInforme o telefone atualizado do contato: ");
        String telefoneAtualizado = "99999-8888"; // menu.next();
        System.out.print("\nInforme a cidade atualizada do contato: ");
        String cidadeAtualizado = "Vitória"; // menu.next();
        System.out.print("\nInforme o país atualizado do contato: ");
        String paisAtualizado = "Brasil"; // menu.next();

        Agenda contato = new Agenda(nomeAtualizado, telefoneAtualizado, cidadeAtualizado, paisAtualizado);

        boolean isAtualizado = this.agenda.atualizar(nomeAtualizado, nome, contato);
        if (isAtualizado) {
            System.out.println("\n\nContato atualizado!");
            return;
        }
        System.out.println("\n\nFalha ao atualizar!");
    }

    private void excluirContato(String nome) {
        Agenda isExcluido = this.agenda.remover(nome);
        if (isExcluido != null) {
            System.out.println("\n\nContato excluido!");
            return;
        }
        System.out.println("\n\nFalha ao excluir, contato não existe na agenda!");
    }

    private void inserirContato(String nome, String telefone, String cidade, String pais) {
        Agenda contato = new Agenda(nome, telefone, cidade, pais);
        boolean isInserido = this.agenda.inserir(nome, contato);
        if (isInserido) {
            System.out.println("\n\nContato inserido!");
            return;
        }
        System.out.println("\n\nFalha ao inserir, contato já existe na agenda!");
    }

    private void localizarContato(String nome) {
        Agenda contato = this.agenda.procurar(nome);
        if (contato == null) {
            System.out.println("\n\nContato não localizado!");
            return;
        }
        System.out.println("\n\nNome Completo: " + contato.getNomeCompleto());
        System.out.println("Telefone: " + contato.getTelefone());
        System.out.println("Cidade: " + contato.getCidade());
        System.out.println("País: " + contato.getPais());
    }

    private int salvarArquivo() {
        try {
            PrintWriter arquivo = new PrintWriter(new FileOutputStream(new File(this.nomeArquivo)));
            ArrayList<Agenda> lista = this.agenda.listar(this.primeiroContato);

            for (Agenda contato : lista) {
                String linhaCsv = contato.getNomeCompleto() + ',' + contato.getTelefone() + ',' + contato.getCidade()
                        + ',' + contato.getPais();
                arquivo.println(linhaCsv);
            }
            arquivo.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return 0;
    }

    private int carregarArquivo(String nomeArquivo) {
        this.nomeArquivo = nomeArquivo;
        boolean primeiroContato = true;
        try {
            BufferedReader arquivo = new BufferedReader(new FileReader(nomeArquivo));

            String linha;
            while ((linha = arquivo.readLine()) != null) {
                String[] valores = linha.split(",");
                String nomeCompleto = valores[0];
                String telefone = valores[1];
                String cidade = valores[2];
                String pais = valores[3];

                if (primeiroContato) {
                    this.primeiroContato = nomeCompleto;
                }

                Agenda pessoaAgenda = new Agenda(nomeCompleto, telefone, cidade, pais);
                this.agenda.inserir(nomeCompleto, pessoaAgenda);
            }

            arquivo.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return 0;
    }
}
