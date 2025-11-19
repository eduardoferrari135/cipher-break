import random
import string
import os
from typing import Tuple, Dict, List
from cipher_breaker import CypherBreaker
from quadgram_scorer import QuadgramScorer


class SubstitutionCypher(CypherBreaker):
    """
    Quebrador de Cifras de Substituição Monoalfabética usando Hill Climbing.
    Espaço de busca: 26! (aprox 4e26 combinações).
    """

    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, message: str):
        super().__init__(message)
        for punct in string.punctuation:
            self.message.replace(punct, "")

        self.message = self.message.upper()

        # Caminho para o arquivo de quadgramas (mesma lógica da classe anterior)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        quadgram_path = os.path.join(current_dir, "..", "data", "english_quadgrams.txt")

        # Inicializa o scorer (assume que a classe QuadgramScorer está disponível no escopo)
        self.scorer = QuadgramScorer(quadgram_path)

    def _decrypt(self, text: str, key_key: str) -> str:
        """
        Decifra o texto usando a chave de substituição fornecida.
        Args:
            key_key: Uma string de 26 chars onde o índice é a letra original
                     e o char é a substituição.
        """
        # Cria tabela de tradução: Cipher Alphabet -> Plain Alphabet
        # O Hill Climbing gera a chave de decifração diretamente
        table = str.maketrans(key_key, self.ALPHABET)
        return text.translate(table)

    def _generate_random_key(self) -> List[str]:
        """Gera uma permutação aleatória do alfabeto"""
        key = list(self.ALPHABET)
        random.shuffle(key)
        return key

    def _hill_climbing(
        self, ciphertext: str, max_iterations: int = 1000, num_restarts: int = 20
    ) -> Tuple[str, float]:
        global_best_key = None
        global_best_score = float("-inf")

        for i in range(num_restarts):
            # 1. Estado inicial aleatório
            current_key_list = self._generate_random_key()
            current_key_str = "".join(current_key_list)

            decrypted = self._decrypt(ciphertext, current_key_str)
            current_score = self.scorer.score(decrypted)

            # 2. Otimização local
            for _ in range(max_iterations):
                # Cria cópia para mutação
                neighbor_key_list = current_key_list[:]

                # Mutação: Swap de dois caracteres aleatórios na chave
                a, b = random.sample(range(26), 2)
                neighbor_key_list[a], neighbor_key_list[b] = (
                    neighbor_key_list[b],
                    neighbor_key_list[a],
                )

                neighbor_key_str = "".join(neighbor_key_list)

                # Avaliação
                decrypted = self._decrypt(ciphertext, neighbor_key_str)
                score = self.scorer.score(decrypted)

                # Aceitação (Hill Climbing estrito)
                if score > current_score:
                    current_score = score
                    current_key_list = neighbor_key_list
                    current_key_str = neighbor_key_str

            # Verifica se este restart encontrou o melhor global
            if current_score > global_best_score:
                global_best_score = current_score
                global_best_key = current_key_str

        return global_best_key, global_best_score

    def break_cypher(self) -> Tuple[str, Dict[str, str]]:
        """
        Executa a quebra da cifra.
        """

        # Otimização da chave
        best_key, score = self._hill_climbing(
            self.message,
            max_iterations=2000,  # Substituição geralmente requer mais iterações que permutação
            num_restarts=30,  # Maior chance de escapar de máximos locais
        )

        # Decifração final
        final_plaintext = self._decrypt(self.message, best_key)

        # Constrói o dicionário de mapeamento (Cipher -> Plain)
        mapping = {}
        for cipher_char, plain_char in zip(best_key, self.ALPHABET):
            mapping[cipher_char] = plain_char

        return final_plaintext, mapping
