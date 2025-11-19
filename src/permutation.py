from cipher_breaker import CypherBreaker
import random
import math
import os
from typing import List, Tuple, Dict
from quadgram_scorer import QuadgramScorer


class PermutationCypher(CypherBreaker):
    def __init__(self, message: str, max_key_length: int = 20) -> None:
        super().__init__(message)
        self.max_key_length = max_key_length

        current_dir = os.path.dirname(os.path.abspath(__file__))
        quadgram_path = os.path.join(current_dir, "..", "data", "english_quadgrams.txt")
        self.scorer = QuadgramScorer(quadgram_path)

    @staticmethod
    def encrypt(text: str, key: List[int]) -> str:
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

    @staticmethod
    def encrypt_block(text: str, key: List[int]) -> str:
        """Cifra usando Permutação de Bloco Simples"""
        clean_text = "".join(c for c in text if c.isalpha()).upper()
        key_len = len(key)
        result = []

        for i in range(0, len(clean_text), key_len):
            chunk = clean_text[i : i + key_len]
            if len(chunk) < key_len:
                result.append(chunk)
            else:
                # A chave [2, 0, 1] significa: 1º char cifrado é o 2º original, etc.
                scrambled_str = "".join([chunk[k] for k in key])
                result.append(scrambled_str)

        return "".join(result)

    def _decrypt_columnar(self, ciphertext: str, key: List[int]) -> str:
        msg_len = len(ciphertext)
        key_len = len(key)

        num_rows = msg_len // key_len
        num_cols_extra = msg_len % key_len

        col_lengths = {}
        for col in range(key_len):
            if col < num_cols_extra:
                col_lengths[col] = num_rows + 1
            else:
                col_lengths[col] = num_rows

        decrypted_cols = [""] * key_len
        current_idx = 0

        for col_idx in key:
            length = col_lengths[col_idx]
            decrypted_cols[col_idx] = ciphertext[current_idx : current_idx + length]
            current_idx += length

        result = []
        for row in range(num_rows + 1):
            for col in range(key_len):
                if row < len(decrypted_cols[col]):
                    result.append(decrypted_cols[col][row])

        return "".join(result)

    def _decrypt_block(self, ciphertext: str, key: List[int]) -> str:
        key_len = len(key)
        msg_len = len(ciphertext)
        result = [""] * msg_len

        inverse_key = [0] * key_len
        for i, k in enumerate(key):
            inverse_key[k] = i

        for i in range(0, msg_len, key_len):
            chunk = ciphertext[i : i + key_len]
            if len(chunk) < key_len:
                for j, char in enumerate(chunk):
                    result[i + j] = char
            else:
                for j, k in enumerate(inverse_key):
                    result[i + j] = chunk[k]

        return "".join(result)

    def _hill_climbing(
        self,
        ciphertext: str,
        key_length: int,
        mode: str = "columnar",
        max_iterations: int = 2000,
        num_restarts: int = 10,
    ) -> Tuple[List[int], float]:
        global_best_key = None
        global_best_score = float("-inf")

        decrypt_func = (
            self._decrypt_columnar if mode == "columnar" else self._decrypt_block
        )

        for restart in range(num_restarts):
            current_key = list(range(key_length))
            random.shuffle(current_key)

            current_decrypted = decrypt_func(ciphertext, current_key)
            current_score = self.scorer.score(current_decrypted)

            improved = True
            while improved:
                improved = False
                best_neighbor_key = None
                best_neighbor_score = float("-inf")

                for i in range(key_length):
                    for j in range(i + 1, key_length):
                        neighbor_key = current_key.copy()
                        neighbor_key[i], neighbor_key[j] = (
                            neighbor_key[j],
                            neighbor_key[i],
                        )

                        text = decrypt_func(ciphertext, neighbor_key)
                        score = self.scorer.score(text)

                        if score > best_neighbor_score:
                            best_neighbor_score = score
                            best_neighbor_key = neighbor_key

                if best_neighbor_score > current_score:
                    current_key = best_neighbor_key
                    current_score = best_neighbor_score
                    improved = True

            if current_score > global_best_score:
                global_best_score = current_score
                global_best_key = current_key

        return global_best_key, global_best_score

    def _find_key_length(self, ciphertext: str) -> Tuple[int, str]:
        best_length = 2
        best_score = float("-inf")
        best_mode = "columnar"

        for length in range(2, min(self.max_key_length + 1, len(ciphertext))):
            _, score_col = self._hill_climbing(
                ciphertext, length, mode="columnar", max_iterations=200, num_restarts=2
            )

            _, score_blk = self._hill_climbing(
                ciphertext, length, mode="block", max_iterations=200, num_restarts=2
            )

            current_best = max(score_col, score_blk)
            mode = "columnar" if score_col >= score_blk else "block"

            if current_best > best_score:
                best_score = current_best
                best_length = length
                best_mode = mode

        return best_length, best_mode

    def break_cypher(self) -> tuple[str, dict[str, str]]:
        clean_text = "".join(c for c in self.message if c.isalpha())

        key_length, mode = self._find_key_length(clean_text)

        best_key, best_score = self._hill_climbing(
            clean_text, key_length, mode=mode, max_iterations=5000, num_restarts=20
        )

        if mode == "columnar":
            decrypted = self._decrypt_columnar(clean_text, best_key)
        else:
            decrypted = self._decrypt_block(clean_text, best_key)

        index_mapping = {}
        for i, k in enumerate(best_key):
            index_mapping[str(i)] = str(k)

        return (decrypted, index_mapping)
