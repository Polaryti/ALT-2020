# -*- coding: utf-8 -*-
import re
import collections
import time

from trie import Trie
import numpy as np
import Tarea2 as t2

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path, n):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        self.vocabulary  = self.build_vocab(vocab_file_path, n, tokenizer=re.compile("\W+"))

    def build_vocab(self, vocab_file_path, n, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero Nde texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """

        tokenizer = re.compile("\W+")
        with open(vocab_file_path, "r", encoding = 'utf-8') as fr:
            c = collections.Counter(tokenizer.split(fr.read().lower()))
            if '' in c:
                del c['']
            reversed_c = [(freq, word) for (word,freq) in c.items()]
            sorted_reversed = sorted(reversed_c, reverse=True)
            sorted_vocab = [word for (freq,word) in sorted_reversed]

            return sorted(sorted_vocab[0: n])

            

    def suggest(self, term, distance="levenshtein", threshold=None):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "restricted", "intermediate"]

        results = {} # diccionario termino:distancia
        if threshold == None: threshold = 2**31
        for voc in self.vocabulary:
            if abs(len(voc)-len(term)) > threshold: d = threshold + 1
            elif distance == "levenshtein":
                d = t2.dp_levenshtein_backwards(term,voc,threshold)
            elif distance == "restricted":
                d = t2.dp_restricted_damerau_backwards(term,voc,threshold)
            else:
                d = t2.dp_intermediate_damerau_backwards(term,voc,threshold)
            if d <= threshold: results[voc] = d
        return results

class TrieSpellSuggester(SpellSuggester):
    def suggest(self, term, distance="levenshtein", threshold=None):
        if distance == "levenshtein":
            results = {}
            if threshold == None: threshold = 2**31
            n = self.trie.get_num_states()
            m = len(term)
            V1 = np.zeros(n)
            V2 = np.zeros(n)
            for i in range(1,n):
                V1[i]= V1[self.trie.get_parent(i)] + 1

            for col in range(1,m + 1):
                V2[0]=col
                for fil in range(1,n) :
                    cost = not term[col-1] == self.trie.get_label(fil)
                    V2[fil] = min(V1[fil] + 1,
                                V2[self.trie.get_parent(fil)] + 1,
                                V1[self.trie.get_parent(fil)] + cost)
                if min(V2) > threshold: return {}
                V1, V2 = V2, V1

            for i in range(n):
                if self.trie.is_final(i):
                    if V1[i] <= threshold: results[self.trie.get_output(i)] = V1[i]
            return results
        else: return super().suggest(term, distance, threshold)
                

    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    """
    def __init__(self, vocab_file_path, n):
        super().__init__(vocab_file_path, n)
        self.trie = Trie(self.vocabulary)
    
if __name__ == "__main__":
    palabras = ("casa", "ancho", "jabón", "vícios")
    tamaños = (5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000)
    thresholds = (1, 2, 3, 5, 7)
    metodos = ("intermediate", "restricted", "levenshtein")
    for p in palabras:
        print(p)
        for x in tamaños: 
            spellsuggester = SpellSuggester("./corpora/quijote.txt", x)    
            for z in metodos:
                for y in thresholds:
                    tini = time.process_time()
                    spellsuggester.suggest(p, z, threshold = y)
                    t = time.process_time() - tini
                    print('Trie: No   Tamaño: '+ str(x) + '   Threshold: ' + str(y) + '   Método: ' + z + '   :   ' + str(t))
            spellsuggester = TrieSpellSuggester("./corpora/quijote.txt", x)
            for y in thresholds:
                tini = time.process_time()
                spellsuggester.suggest(p, "levenshtein", threshold = y)
                t = time.process_time() - tini
                print('Trie: Sí   Tamaño: '+ str(x) + '   Threshold: ' + str(y) + '   Método: levenshtein   :   ' + str(t))

