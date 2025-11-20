# Quebra de Cifras: Substituição e Permutação

Este projeto implementa algoritmos de criptoanálise para quebrar cifras clássicas de **Substituição Monoalfabética** e **Permutação Livre**, sem conhecimento prévio da chave.

O sistema utiliza técnicas de otimização estocástica (**Hill Climbing**) guiadas por estatística de linguagem (**Quadgrams**) para recuperar o texto original.

---

## 1. O Processo de Cifragem

O projeto aborda duas categorias fundamentais de criptografia clássica:

### A. Cifra de Substituição
Cada letra do alfabeto original é mapeada para uma letra diferente. A estrutura das palavras muda, mas a frequência das letras é preservada (mas mascarada).
* **Exemplo:** `HELLO` -> (A=X, B=Y...) -> `XUBBU`

### B. Cifra de Permutação (Livre)
Os caracteres permanecem os mesmos, mas suas posições são alteradas seguindo uma regra geométrica ou matricial.
* **Abrangência:** O algoritmo foi desenhado para cobrir *Transposição Colunar*, *Rail Fence*, *Rotações* e *Blocos*, tratando todas como uma matriz de colunas reordenadas.
* **Exemplo:** `HELLO` -> (reordenar) -> `LHLEO`

---

## 2. O Processo de Quebra

O ataque ignora a força bruta (que seria impossível para $26!$ combinações na substituição) e utiliza um método iterativo inteligente.

### O Motor: Quadgram Scoring
Para saber se uma tentativa de decriptação está correta, o algoritmo calcula um *score* baseado na probabilidade de sequências de 4 letras (Quadgrams) em inglês.
* `THEY` tem pontuação alta.
* `XQKZ` tem pontuação baixa.

### Algoritmo 1: Quebra de Substituição
1.  **Inicialização:** Começa com uma chave aleatória.
2.  **Mutação:** Troca duas letras da chave de lugar.
3.  **Avaliação:** Se o texto decifrado tem um *score* melhor, mantém a troca. Caso contrário, desfaz.
4.  **Restarts:** Repete o processo várias vezes para evitar ficar preso em máximos locais.

### Algoritmo 2: Quebra de Permutação
Como o tamanho da chave é desconhecido, o algoritmo adota uma estratégia dinâmica:
1.  **Busca de Período:** Testa tamanhos de chave de 2 até um limite (ex: 15).
2.  **Abordagem Matricial:** Para cada tamanho, trata o texto como uma grade de colunas.
3.  **Otimização:** Usa Hill Climbing para encontrar a melhor ordem dessas colunas.
    * Essa abordagem resolve geometricamente cifras como *Rail Fence* e *Leitura em Z*, pois elas geram padrões periódicos equivalentes a uma transposição de colunas.

---

## 3. Executando o Projeto

Certifique-se de que o arquivo `english_quadgrams.txt` esteja na pasta `data/`.

Para rodar a demonstração completa (que cifra e depois quebra automaticamente):

```bash
python main.py