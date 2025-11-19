import math


class QuadgramScorer:
    """Classe para calcular fitness usando quadgramas ingleses"""

    def __init__(self, quadgram_file: str):
        self.quadgrams = {}
        self.N = 0
        self.floor = None
        self._load_quadgrams(quadgram_file)

    def _load_quadgrams(self, filename: str):
        """Carrega quadgramas do arquivo e calcula log probabilities"""
        with open(filename, "r", encoding="utf-8") as f:
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
        text = text.upper().replace(" ", "")
        score = 0

        for i in range(len(text) - 3):
            quadgram = text[i : i + 4]
            if quadgram in self.quadgrams:
                score += self.quadgrams[quadgram]
            else:
                score += self.floor

        return score
