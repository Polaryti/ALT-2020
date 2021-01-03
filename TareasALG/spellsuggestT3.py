# -*- coding: utf-8 -*-
import re

import numpy as np
import Tarea3 as t3
from optimistBounds import hamming_distance

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        self.vocabulary  = self.build_vocab(vocab_file_path, tokenizer=re.compile(r"\W+"))

    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('') # por si acaso
            return sorted(vocab)

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
            if abs(len(voc)-len(term)) > threshold or hamming_distance(term, voc) > threshold:
                d = threshold + 1
            elif distance == "levenshtein":
                d = t3.dp_levenshtein_backwards(term, voc, threshold)
            elif distance == "restricted":
                d = t3.dp_restricted_damerau_backwards(term, voc, threshold)
            else:
                d = t3.dp_intermediate_damerau_backwards(term, voc, threshold)

            if d <= threshold:
                results[voc] = d

        return results
    
if __name__ == "__main__":
    spellsuggester = SpellSuggester("./corpora/quijote.txt")
    results = spellsuggester.suggest("casa", "intermediate", threshold = 3)
    results_sorted = dict(sorted(results.items(), key=lambda item: item[1]))
    print(f"{'Word':10} | {'Dist':4}")
    print(f"{'-'*17}")
    for i in results_sorted:
        print(f"{i:10} | {results[i]:4}")
    print(f"{'-'*17}")
    print(f"Length: {len(results)}")
