import os
import random
from typing import List, Tuple, Union
from cipher_breaker import CypherBreaker
from quadgram_scorer import QuadgramScorer


class PermutationCypher(CypherBreaker):
    def __init__(self, message: str, max_key_length: int = 15) -> None:
        super().__init__(message)
        self.max_key_length = max_key_length

        current_dir = os.path.dirname(os.path.abspath(__file__))
        quadgram_path = os.path.join(current_dir, "..", "data", "english_quadgrams.txt")
        
        if not os.path.exists(quadgram_path):
            quadgram_path = os.path.join(current_dir, "english_quadgrams.txt")
            
        self.scorer = QuadgramScorer(quadgram_path)

    @staticmethod
    def encrypt(text: str, key: List[int]) -> str:
        """
        Implementação da encriptação por transposição colunar.
        """
        clean_text = "".join(c for c in text if c.isalpha()).upper()
        key_len = len(key)
        
        rows = [clean_text[i : i + key_len] for i in range(0, len(clean_text), key_len)]
        
        ciphertext = []
        for k in key:
            col_chars = []
            for row in rows:
                if k < len(row):
                    col_chars.append(row[k])
            ciphertext.append("".join(col_chars))
            
        return "".join(ciphertext)

    def _generic_decrypt(self, data: Union[str, List[int]], key: List[int]) -> Union[str, List[int]]:
        """
        Decripta assumindo uma transposição genérica de colunas.
        Funciona tanto para texto (str) quanto para lista de índices (List[int]).
        """
        is_string = isinstance(data, str)
        sequence = list(data) if is_string else data
        
        msg_len = len(sequence)
        key_len = len(key)

        # 1. Calcular dimensões da matriz
        num_rows = msg_len // key_len
        num_cols_extra = msg_len % key_len

        # 2. Determinar o tamanho de cada coluna
        col_lengths = {}
        for col in range(key_len):
            if col < num_cols_extra:
                col_lengths[col] = num_rows + 1
            else:
                col_lengths[col] = num_rows

        # 3. Fatiar a sequência nas colunas baseadas na chave
        cols_data = [None] * key_len
        current_idx = 0
        
        for k in key:
            length = col_lengths[k]
            cols_data[k] = sequence[current_idx : current_idx + length]
            current_idx += length

        # 4. Reconstruir lendo linha por linha
        result = []
        for row in range(num_rows + 1):
            for col in range(key_len):
                if row < len(cols_data[col]):
                    result.append(cols_data[col][row])

        if is_string:
            return "".join(result)
        return result

    def _hill_climbing(self, ciphertext: str, key_len: int, max_iterations: int = 500) -> Tuple[List[int], float]:
        """
        Executa o algoritmo Hill Climbing para encontrar a melhor permutação
        dado um tamanho de chave fixo.
        """
        # Estado inicial aleatório
        current_key = list(range(key_len))
        random.shuffle(current_key)

        current_text = self._generic_decrypt(ciphertext, current_key)
        current_score = self.scorer.score(current_text)

        # Otimização
        for _ in range(max_iterations):
            # Mutação: troca dois índices de lugar
            neighbor_key = current_key.copy()
            i, j = random.sample(range(key_len), 2)
            neighbor_key[i], neighbor_key[j] = neighbor_key[j], neighbor_key[i]

            decrypted_text = self._generic_decrypt(ciphertext, neighbor_key)
            score = self.scorer.score(decrypted_text)

            if score > current_score:
                current_score = score
                current_key = neighbor_key

        return current_key, current_score

    def break_cypher(self) -> tuple[str, dict[str, str]]:
        """
        Método principal: Tenta quebrar a cifra testando vários tamanhos de chave.
        Retorna o texto decifrado e o mapa de índices.
        """
        clean_text = "".join(c for c in self.message if c.isalpha()).upper()
        
        best_global_score = float("-inf")
        best_global_key = []
        
        # Limita o teste de chaves para não exceder o tamanho da mensagem
        limit = min(self.max_key_length, len(clean_text) // 2)

        # 1. Busca pelo período (Key Length)
        for length in range(2, limit + 1):
            # Restarts: Roda o hill climbing algumas vezes para cada tamanho para evitar máximos locais.
            restarts = 5 if length < 8 else 10
            
            for _ in range(restarts):
                key, score = self._hill_climbing(clean_text, length)
                
                if score > best_global_score:
                    best_global_score = score
                    best_global_key = key

        # 2. Decriptação final com a melhor chave encontrada
        final_text = self._generic_decrypt(clean_text, best_global_key)

        # 3. Geração do Mapeamento de Índices
        original_indices = list(range(len(clean_text)))
        
        permuted_indices = self._generic_decrypt(original_indices, best_global_key)
        
        # Mapeia: Onde estava no cifrado (chave) -> Onde ficou no decifrado (valor)
        index_mapping = {}
        for new_pos, original_pos in enumerate(permuted_indices):
            index_mapping[str(original_pos)] = str(new_pos)

        return str(final_text), index_mapping