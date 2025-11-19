from cipher_breaker import CypherBreaker
import random
import math
import os
from typing import List, Tuple, Dict


class QuadgramScorer:
    """Classe para calcular fitness usando quadgramas ingleses"""
    
    def __init__(self, quadgram_file: str):
        self.quadgrams = {}
        self.N = 0
        self.floor = None
        self._load_quadgrams(quadgram_file)
    
    def _load_quadgrams(self, filename: str):
        """Carrega quadgramas do arquivo e calcula log probabilities"""
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    quadgram, count = parts[0], int(parts[1])
                    self.quadgrams[quadgram] = count
                    self.N += count
        
        # Converter para log probabilities para melhor performance
        for key in self.quadgrams:
            self.quadgrams[key] = math.log10(self.quadgrams[key] / self.N)
        
        # Floor value para quadgramas não encontrados
        self.floor = math.log10(0.01 / self.N)
    
    def score(self, text: str) -> float:
        """Calcula o score de fitness do texto baseado em quadgramas"""
        text = text.upper().replace(' ', '')
        score = 0
        
        for i in range(len(text) - 3):
            quadgram = text[i:i+4]
            if quadgram in self.quadgrams:
                score += self.quadgrams[quadgram]
            else:
                score += self.floor
        
        return score


class PermutationCypher(CypherBreaker):
    """Quebrador de cifras de permutação usando Simulated Annealing"""
    
    def __init__(self, message: str, max_key_length: int = 20) -> None:
        super().__init__(message)
        self.max_key_length = max_key_length
        
        # Caminho para o arquivo de quadgramas
        current_dir = os.path.dirname(os.path.abspath(__file__))
        quadgram_path = os.path.join(current_dir, '..', 'data', 'english_quadgrams.txt')
        self.scorer = QuadgramScorer(quadgram_path)
    
    @staticmethod
    def encrypt(text: str, key: List[int]) -> str:
        """
        Cifra o texto usando Transposição Colunar com a chave fornecida.
        Remove caracteres não alfabéticos antes de cifrar.
        """
        # Limpa o texto mantendo apenas letras
        clean_text = ''.join(c for c in text if c.isalpha()).upper()
        key_len = len(key)
        
        # Cria as linhas da grade
        rows = [clean_text[i:i+key_len] for i in range(0, len(clean_text), key_len)]
        
        # Lê as colunas na ordem especificada pela chave
        ciphertext = []
        for k in key:
            # k é o índice da coluna a ser lida
            col_chars = []
            for row in rows:
                if k < len(row):
                    col_chars.append(row[k])
            ciphertext.append("".join(col_chars))
        
        return "".join(ciphertext)

    def _decrypt_columnar(self, ciphertext: str, key: List[int]) -> str:
        """
        Decifra Transposição Colunar Irregular
        
        Args:
            ciphertext: Texto cifrado
            key: Lista de inteiros indicando a ordem das colunas (ex: [2, 0, 1])
                 Significa que a 1ª coluna lida foi a coluna original 2, depois a 0, etc.
        """
        msg_len = len(ciphertext)
        key_len = len(key)
        
        # Número de linhas completas e colunas que têm uma célula extra
        num_rows = msg_len // key_len
        num_cols_extra = msg_len % key_len
        
        # Determina o tamanho de cada coluna original
        # As primeiras 'num_cols_extra' colunas originais têm (num_rows + 1) elementos
        # As restantes têm 'num_rows' elementos
        col_lengths = {}
        for col in range(key_len):
            if col < num_cols_extra:
                col_lengths[col] = num_rows + 1
            else:
                col_lengths[col] = num_rows
        
        # O texto cifrado é a concatenação das colunas na ordem especificada pela chave.
        # Precisamos reconstruir as colunas originais.
        
        # Primeiro, vamos descobrir onde cortar o ciphertext para pegar cada coluna.
        # A chave diz a ordem. Ex: key=[2, 0, 1]. 
        # O ciphertext começa com a coluna 2, depois coluna 0, depois coluna 1.
        
        decrypted_cols = [''] * key_len
        current_idx = 0
        
        for col_idx in key:
            length = col_lengths[col_idx]
            decrypted_cols[col_idx] = ciphertext[current_idx : current_idx + length]
            current_idx += length
            
        # Agora lemos a matriz por linhas para reconstruir o plaintext
        result = []
        for row in range(num_rows + 1):
            for col in range(key_len):
                # Se esta coluna tem caracteres suficientes para esta linha
                if row < len(decrypted_cols[col]):
                    result.append(decrypted_cols[col][row])
                    
        return ''.join(result)

    def _hill_climbing(self, ciphertext: str, key_length: int, 
                      max_iterations: int = 2000,
                      num_restarts: int = 10) -> Tuple[List[int], float]:
        """
        Implementa Hill Climbing para Transposição Colunar
        """
        global_best_key = None
        global_best_score = float('-inf')
        
        for restart in range(num_restarts):
            # Inicializa com uma permutação aleatória
            current_key = list(range(key_length))
            random.shuffle(current_key)
            
            # Decifra e avalia
            current_decrypted = self._decrypt_columnar(ciphertext, current_key)
            current_score = self.scorer.score(current_decrypted)
            
            # Loop de otimização
            improved = True
            while improved:
                improved = False
                best_neighbor_key = None
                best_neighbor_score = float('-inf')
                
                # Tenta todas as trocas possíveis (vizinhança)
                for i in range(key_length):
                    for j in range(i + 1, key_length):
                        # Troca
                        neighbor_key = current_key.copy()
                        neighbor_key[i], neighbor_key[j] = neighbor_key[j], neighbor_key[i]
                        
                        # Avalia
                        text = self._decrypt_columnar(ciphertext, neighbor_key)
                        score = self.scorer.score(text)
                        
                        if score > best_neighbor_score:
                            best_neighbor_score = score
                            best_neighbor_key = neighbor_key
                
                # Se encontrou um vizinho melhor que o atual, move para ele
                if best_neighbor_score > current_score:
                    current_key = best_neighbor_key
                    current_score = best_neighbor_score
                    improved = True
            
            # Fim do hill climbing local, verifica se é o melhor global
            if current_score > global_best_score:
                global_best_score = current_score
                global_best_key = current_key
                
        return global_best_key, global_best_score

    def _find_key_length(self, ciphertext: str) -> int:
        """
        Tenta encontrar o comprimento mais provável da chave
        """
        best_length = 2
        best_score = float('-inf')
        
        print("Analisando tamanhos de chave...")
        
        # Testa tamanhos de 2 até max_key_length
        for length in range(2, min(self.max_key_length + 1, len(ciphertext))):
            # Executa um HC rápido (menos restarts)
            key, score = self._hill_climbing(
                ciphertext, 
                length, 
                max_iterations=500, 
                num_restarts=3
            )
            
            print(f"Tamanho {length:2d}: score {score:.2f}")
            
            if score > best_score:
                best_score = score
                best_length = length
                
        print(f"Melhor tamanho detectado: {best_length}\n")
        return best_length
    
    def break_cypher(self) -> tuple[str, dict[str, str]]:
        """
        Quebra a cifra de permutação
        """
        print("=" * 60)
        print("QUEBRADOR DE CIFRA DE PERMUTAÇÃO (HILL CLIMBING)")
        print("=" * 60)
        print(f"\nTexto cifrado: {self.message[:100]}...")
        print(f"Tamanho: {len(self.message)} caracteres\n")
        
        clean_text = ''.join(c for c in self.message if c.isalpha())
        
        # 1. Encontra o tamanho da chave
        key_length = self._find_key_length(clean_text)
        
        # 2. Otimiza a chave com o tamanho encontrado
        print(f"Otimizando chave de tamanho {key_length}...")
        best_key, best_score = self._hill_climbing(
            clean_text,
            key_length,
            max_iterations=5000,
            num_restarts=20  # Mais restarts para garantir o global optimum
        )
        
        # 3. Decifra com a melhor chave
        decrypted = self._decrypt_columnar(clean_text, best_key)
        
        # Cria mapeamento
        index_mapping = {}
        for i, k in enumerate(best_key):
            index_mapping[str(i)] = str(k)
        
        return (decrypted, index_mapping)