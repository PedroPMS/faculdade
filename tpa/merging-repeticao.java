import java.util.*;

public class Main {
  public static void main(String[] args) {
    ArrayList<Integer> lista_1 = gerarArrayAleatorio(10, 15);
    ArrayList<Integer> lista_2 = gerarArrayAleatorio(10, 15);
    ArrayList<Integer> lista_3 = gerarArrayAleatorio(10, 15);
    System.out.println("1 número de elementos: "+lista_1);
    System.out.println("2 número de elementos: "+lista_2);
    System.out.println("3 número de elementos: "+lista_3);

    ArrayList<Integer> merging = new ArrayList<Integer>();

    long startTime = System.nanoTime();

    merging = merging(lista_1, lista_2);
    merging = merging(merging, lista_3);
    long endTime = System.nanoTime();

    long duration = (endTime - startTime);
    System.out.println("Merging número de elementos: "+merging);
    // System.out.println("Duração: "+duration/1000000+" ms");

  }

  public static ArrayList<Integer> merging(ArrayList<Integer> lista_a, ArrayList<Integer> lista_b) {
    ArrayList<Integer> saida = new ArrayList<>();
    int i = 0;
    int j = 0;

    // Enquanto nenhuma das lista chegar ao fim
    while(i < lista_a.size() && j < lista_b.size()) {
        if(lista_a.get(i) < lista_b.get(j)) {
            inserirElementoNoArray(saida, lista_a.get(i));
            i++;
        } else if(lista_a.get(i) > lista_b.get(j)) {
            inserirElementoNoArray(saida, lista_b.get(j));
            j++;
        } else {
            inserirElementoNoArray(saida, lista_a.get(i));
            inserirElementoNoArray(saida, lista_b.get(j));
            i++;
            j++;
        }
    }
    
    saida = inserirElementoRestantes(saida, lista_a, i);
    saida = inserirElementoRestantes(saida, lista_b, j);

    return saida;
  }
  
  
  // Insere os elementos restantes de uma lista que não foram percorridos no while. Ex: lista A chegou ao fim, todos os outros elementos da lista B vão ser inseridos
  public static ArrayList<Integer> inserirElementoRestantes(ArrayList<Integer> saida, ArrayList<Integer> lista, int posicaoInicial) {
    int i;
    
    if(posicaoInicial < lista.size()) {
        for(i=posicaoInicial; i < lista.size(); i++) {
            inserirElementoNoArray(saida, lista.get(i));
        }
    }
    return saida;
  }
  

  // Insere um novo elemente no array se esse elemento não já existir
  public static ArrayList<Integer> inserirElementoNoArray(ArrayList<Integer> array, int item) {
      array.add(item);
    return array;
  }

  // Método para gerar um array com valores aleatórios
  public static ArrayList<Integer> gerarArrayAleatorio(int tamanhoArray, int max) {
    ArrayList<Integer> array = new ArrayList<Integer>(tamanhoArray);
    Random random = new Random();
    int min = 1;
    
    for (int i = 0; i < tamanhoArray; i++) {
      array.add((int) Math.floor(Math.random()*(max-min+1)+min));
    }

    Collections.sort(array);
    return array;
  }
}
