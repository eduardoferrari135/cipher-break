from substitution import SubstitutionCypher
from permutation import PermutationCypher


def test_permutation_cipher():
    """Testa o quebrador de cifra de permutação"""
    
    print("\n" + "="*60)
    print("TESTE 1: Transposição por Colunas")
    print("="*60)
    
    # Definindo texto e chave originais
    original_text1 = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    key1 = [3, 0, 4, 1, 2]
    
    ciphertext1 = PermutationCypher.encrypt(original_text1, key1)
    
    # 1. Texto Original
    print(f"\nTexto Original:\n{original_text1}")
    
    # 2. Texto Cifrado
    print(f"\nTexto Cifrado:\n{ciphertext1}")
    
    print("\nAlgoritmo de Quebra:")
    # 3. Algoritmo de quebra (Logs internos serão impressos aqui)
    breaker1 = PermutationCypher(ciphertext1, max_key_length=10)
    decrypted1, mapping1 = breaker1.break_cypher()
    
    # 4. Índice de cada letra (mapeamento)
    print(f"Mapeamento de Índices (Posição Cifrada -> Coluna Original):")
    print(f"{mapping1}")
    
    # 5. Texto Decifrado
    print(f"\nTexto Decifrado com o Algoritmo:\n{decrypted1}")
    
    
    print("\n\n" + "="*60)
    print("TESTE 2: Texto Mais Longo")
    print("="*60)
    
    original_text2 = "CRYPTOGRAPHY IS THE PRACTICE OF SECURE COMMUNICATION IN THE PRESENCE OF THIRD PARTIES"
    key2 = [2, 0, 3, 1, 4]
    
    ciphertext2 = PermutationCypher.encrypt(original_text2, key2)
    
    print(f"\nTexto Original:\n{original_text2}")
    print(f"\nTexto Cifrado:\n{ciphertext2}")
    
    print("\nAlgoritmo de Quebra:")
    breaker2 = PermutationCypher(ciphertext2, max_key_length=12)
    decrypted2, mapping2 = breaker2.break_cypher()
    
    print(f"Mapeamento de Índices (Posição Cifrada -> Coluna Original):")
    print(f"{mapping2}")
    
    print(f"\nTexto Decifrado com o Algoritmo:\n{decrypted2}")
    
    
    print("\n\n" + "="*60)
    print("TESTE 3: Permutação de Bloco (Block Cipher)")
    print("="*60)
    
    original_text3 = "THIS IS A TEST OF THE BLOCK PERMUTATION CIPHER WHICH IS DIFFERENT FROM COLUMNAR"
    key3 = [3, 0, 4, 1, 2]
    
    ciphertext3 = PermutationCypher.encrypt_block(original_text3, key3)
    
    print(f"\nTexto Original:\n{original_text3}")
    print(f"\nTexto Cifrado (Bloco):\n{ciphertext3}")
    
    print("\nAlgoritmo de Quebra:")
    breaker3 = PermutationCypher(ciphertext3, max_key_length=10)
    decrypted3, mapping3 = breaker3.break_cypher()
    
    print(f"Mapeamento de Índices:")
    print(f"{mapping3}")
    
    print(f"\nTexto Decifrado:\n{decrypted3}")


def test_substitution_cipher():
    """Testa o quebrador de cifra de substituição (a ser implementado)"""
    print("\n" + "="*60)
    print("TESTE DE CIFRA DE SUBSTITUIÇÃO")
    print("="*60)
    print("(Ainda não implementado)")


if __name__ == "__main__":
    
    # Testa quebra de cifra de permutação
    test_permutation_cipher()
    
    # Descomente para testar cifra de substituição quando implementada
    # test_substitution_cipher()
