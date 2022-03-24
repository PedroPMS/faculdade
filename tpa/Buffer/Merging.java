import java.util.*;

public class Merging {
    public void mergeBuffers(ArrayList<Buffer> buffers, Buffer bufferSaida) {
        iniciarLeitura(buffers);

        ArrayList<String> items = getItemsBuffers(buffers);

        // Enquanto tiverem itens nos buffers
        while (items.size() > 0) {
            String menorItem = Collections.min(items);

            merge(buffers, menorItem, bufferSaida);
            items = getItemsBuffers(buffers);
        }
    }

    // Inicia a leitura dos arquivos, fazendo o read em todos os buffers
    private void iniciarLeitura(ArrayList<Buffer> buffers) {
        for (int i = 0; i < buffers.size(); i++) {
            buffers.get(i).read();
        }
    }

    // Pega os itens das posições atuais (getCurrent) dos buffers de leitura e
    // carrega para uma lista de itens
    private ArrayList<String> getItemsBuffers(ArrayList<Buffer> buffers) {

        int i;
        ArrayList<String> items = new ArrayList<String>();
        for (i = 0; i < buffers.size(); i++) {
            Agenda itemBuffer = buffers.get(i).getCurrent();
            if (itemBuffer != null) {
                items.add(itemBuffer.getNomeCompleto());
            }
        }
        return items;
    }

    // Escreve o menor item na saída e avança a leitura em todos os buffers em que a
    // cabeça de leitura é igual ao item
    public void merge(ArrayList<Buffer> buffers, String menorItem, Buffer bufferSaida) {
        for (int j = 0; j < buffers.size(); j++) {
            // Pega o item atual de cada buffer
            Agenda itemBuffer = buffers.get(j).getCurrent();
            if (itemBuffer == null) {
                continue;
            }

            String item = itemBuffer.getNomeCompleto();
            // System.out.println("buffer" + j + ", " + menorItem + ", " + item);
            // Se o item atual do buffer for igual ao menorItem atual, avança a leitura no
            // buffer
            if (item.compareTo(menorItem) == 0) {
                buffers.get(j).read();

                bufferSaida.write(itemBuffer);
            }
        }
    }
}
