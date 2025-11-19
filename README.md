# Quebra de Cifra de Permutação

Este projeto implementa um algoritmo para quebrar cifras de permutação, sem conhecimento prévio da chave ou do método utilizado.

O processo é dividido em duas etapas principais:
1. **Cifragem (para validação):** Geramos um texto cifrado a partir de um texto original (usando Transposição Colunar ou Permutação de Bloco).
2. **Quebra (ataque):** O algoritmo descobre o método, o tamanho da chave e a chave em si, recuperando o texto original.

---

## 1. O Processo de Cifragem

O sistema suporta dois tipos de embaralhamento:

### A. Transposição Colunar
O texto é escrito em linhas e lido por colunas embaralhadas.
*   **Exemplo:** `HELLO` -> (grade) -> lê colunas -> `LHOEL`

### B. Permutação de Bloco
O texto é dividido em blocos pequenos (ex: 5 letras) e as letras são embaralhadas dentro de cada bloco, sempre com a mesma regra.
*   **Exemplo:** `HELLO` -> (troca posições 1 e 2) -> `HLELO`

---

## 2. O Processo de Quebra

O ataque é baseado em **Hill Climbing** guiado por **Análise de Frequência de Quadgramas**. Ele é "universal" porque testa múltiplas hipóteses.

### Passo 1: Detecção de Configuração
O algoritmo testa combinações de:
*   **Tamanho da Chave:** de 2 até 20.
*   **Modo:** Colunar vs. Bloco.

Para cada combinação, ele faz uma decifragem rápida e avalia se o texto resultante "parece" inglês (usando quadgramas). A melhor combinação vence.

### Passo 2: Descobrir a Chave (Otimização)
Com o tamanho e o modo definidos, o algoritmo refina a chave:
1.  Começa com uma chave aleatória.
2.  Troca duas posições da chave e vê se o texto melhora.
3.  Se melhorar, mantém. Se não, desfaz.
4.  Repete até encontrar a melhor chave possível.

### Passo 3: Decifragem Final
Aplica a melhor chave encontrada usando o modo detectado para revelar a mensagem original.

---

## 3. Executando o Projeto

Para ver o processo acontecendo, execute:

```bash
python3 main.py
```

Isso rodará testes automatizados que:
1.  Cifram textos usando Transposição Colunar e Permutação de Bloco.
2.  O algoritmo analisa e quebra cada um automaticamente.
3.  Exibe o texto recuperado e qual método foi detectado.

### Estrutura dos Arquivos

*   `src/permutation.py`: Implementação do algoritmo (Cifragem, Decifragem Universal, Hill Climbing).
*   `src/main.py`: Script de teste com exemplos variados.
*   `data/english_quadgrams.txt`: Banco de dados de frequências de quadgramas.
