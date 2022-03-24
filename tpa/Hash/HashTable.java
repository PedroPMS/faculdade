import java.util.ArrayList;

public class HashTable<Key extends Comparable<? super Key>, E> {
    private int tamanhoHashTable;
    private KVpair<Key, E>[] HT;
    private KVpair<Key, E> KVVazio = new KVpair<Key, E>();

    private int h(Key key) {
        return tamanhoHashTable - 1;
    }

    private int p(Key key, int slot) {
        return slot;
    }

    @SuppressWarnings("unchecked")
    HashTable(int t) {
        tamanhoHashTable = t;
        HT = (KVpair<Key, E>[]) new KVpair[tamanhoHashTable];
    }

    /** Insere um novo registro com a chave k e valor r na HashTable */
    boolean inserir(Key k, E r) {
        int home;
        int pos = home = h(k); // Posição inicial
        for (int i = 1; HT[pos] != null && HT[pos] != KVVazio; i++) {
            if (HT[pos].key().compareTo(k) == 0) {
                // Essa chave já existe na tabela
                return false;
            }
            assert HT[pos].key().compareTo(k) != 0 : "Duplicates not allowed";
            pos = (home + p(k, i)) % tamanhoHashTable; // Calcula a próxima possível posição
        }
        HT[pos] = new KVpair<Key, E>(k, r); // Insere na HashTable
        return true;
    }

    boolean atualizar(Key kAtt, Key KOld, E r) {
        // Remove registro antigo da HashTable
        E removido = remover(KOld);
        System.out.println(removido);
        // Se a chave antiga não existir, desconsidera a atualização
        if (removido == null) {
            return false;
        }
        // Insere o par atualizado na HashTable
        return inserir(kAtt, r);
    }

    /** Removev o registro com a chave k */
    E remover(Key k) {
        int home;
        int pos = home = h(k); // Posição inicial
        for (int i = 1; (HT[pos] != null) && (HT[pos] == KVVazio || HT[pos].key().compareTo(k) != 0); i++)
            pos = (home + p(k, i)) % tamanhoHashTable; // Calcula a próxima possível posição
        if (HT[pos] == null)
            return null; // A chave não está na HashTable
        else { // Encontou
            E e = HT[pos].value();
            HT[pos] = KVVazio;
            return e;
        }
    }

    /** Procura pelo registro com a chave k */
    E procurar(Key k) {
        int home;
        int pos = home = h(k); // Posição inicial
        for (int i = 1; (HT[pos] != null) && (HT[pos] == KVVazio || HT[pos].key().compareTo(k) != 0); i++)
            pos = (home + p(k, i)) % tamanhoHashTable; // Calcula a próxima possível posição
        if (HT[pos] == null)
            return null; // A chave não está na HashTable
        else
            return HT[pos].value(); // Encontou
    }

    /** Procura pelo registro com a chave k */
    ArrayList<E> listar(Key k) {
        ArrayList<E> lista = new ArrayList<E>();
        int home;
        int pos = home = h(k); // Posição inicial
        for (int i = 1; i < tamanhoHashTable && (HT[pos] != null); i++) {
            if (HT[pos] != KVVazio) {
                E e = HT[pos].value();
                lista.add(e);
            }

            pos = (home + p(k, i)) % tamanhoHashTable; // Calcula a próxima possível posição
        }
        return lista;
    }
}
