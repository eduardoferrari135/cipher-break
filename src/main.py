import permutation
from substitution import SubstitutionCypher
from permutation import PermutationCypher
import substitution


def test_permutation_cipher():
    """Testa o quebrador de cifra de permutação"""
    print("\n" + "_" * 60)
    print("TESTES PERMUTAÇÃO")
    print("_" * 60)

    print("\n" + "=" * 60)
    print("TESTE 1: Transposição por Colunas")
    print("=" * 60)

    # Definindo texto e chave originais
    original_text1 = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    key1 = [3, 0, 4, 1, 2]

    ciphertext1 = PermutationCypher.encrypt(original_text1, key1)

    # 1. Texto Original
    print(f"\nTexto Original:\n{original_text1}")

    # 2. Texto Cifrado
    print(f"\nTexto Cifrado:\n{ciphertext1}")

    # 3. Algoritmo de quebra (Logs internos serão impressos aqui)
    breaker1 = PermutationCypher(ciphertext1, max_key_length=10)
    decrypted1, mapping1 = breaker1.break_cypher()

    # 4. Índice de cada letra (mapeamento)
    print("Mapeamento de Índices (Posição Cifrada -> Coluna Original):")
    print(f"{mapping1}")

    # 5. Texto Decifrado
    print(f"\nTexto Decifrado com o Algoritmo:\n{decrypted1}")

    print("\n\n" + "=" * 60)
    print("TESTE 2: Texto Mais Longo")
    print("=" * 60)

    original_text2 = "CRYPTOGRAPHY IS THE PRACTICE OF SECURE COMMUNICATION IN THE PRESENCE OF THIRD PARTIES"
    key2 = [2, 0, 3, 1, 4]

    ciphertext2 = PermutationCypher.encrypt(original_text2, key2)

    print(f"\nTexto Original:\n{original_text2}")
    print(f"\nTexto Cifrado:\n{ciphertext2}")

    print("\nAlgoritmo de Quebra:")
    breaker2 = PermutationCypher(ciphertext2, max_key_length=12)
    decrypted2, mapping2 = breaker2.break_cypher()

    print("Mapeamento de Índices (Posição Cifrada -> Coluna Original):")
    print(f"{mapping2}")

    print(f"\nTexto Decifrado com o Algoritmo:\n{decrypted2}")

    print("\n\n" + "=" * 60)
    print("TESTE 3: Permutação de Bloco (Block Cipher)")
    print("=" * 60)

    original_text3 = "THIS IS A TEST OF THE BLOCK PERMUTATION CIPHER WHICH IS DIFFERENT FROM COLUMNAR"
    key3 = [3, 0, 4, 1, 2]

    ciphertext3 = PermutationCypher.encrypt_block(original_text3, key3)

    print(f"\nTexto Original:\n{original_text3}")
    print(f"\nTexto Cifrado (Bloco):\n{ciphertext3}")

    print("\nAlgoritmo de Quebra:")
    breaker3 = PermutationCypher(ciphertext3, max_key_length=10)
    decrypted3, mapping3 = breaker3.break_cypher()

    print("Mapeamento de Índices:")
    print(f"{mapping3}")

    print(f"\nTexto Decifrado:\n{decrypted3}")


def test_substitution_cipher():
    """Testa o quebrador de cifra de substituição com formatação padronizada"""
    import random

    print("\n" + "_" * 60)
    print("TESTES SUBSTITUIÇÃO")
    print("_" * 60)

    print("\n" + "=" * 60)
    print("TESTE 1: Cifra de Substituição (Hill Climbing)")
    print("=" * 60)

    # --- Configuração dos Dados ---
    plaintext = (
        "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES FOR SECURE COMMUNICATION "
        "IN THE PRESENCE OF ADVERSARIAL BEHAVIOR MORE GENERALLY CALLED THIRD PARTIES "
        "MODERN CRYPTOGRAPHY EXISTS AT THE INTERSECTION OF THE DISCIPLINES OF MATHEMATICS "
    )

    # Remove espaços para simular dificuldade real

    # Gera chave aleatória
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key_list = list(alphabet)
    random.shuffle(key_list)
    target_key = "".join(key_list)

    # Cifra o texto
    encrypt_table = str.maketrans(alphabet, target_key)
    ciphertext = plaintext.translate(encrypt_table)

    # 1. Texto Original
    # Mostramos apenas os primeiros 100 chars para não poluir o console
    print(f"\nTexto Original:\n{plaintext[:100]}...")

    # 2. Texto Cifrado e Chave Real
    print(f"\nTexto Cifrado:\n{ciphertext[:100]}...")
    print(f"\nChave (Gerada Aleatoriamente):\n{target_key}")

    breaker = SubstitutionCypher(ciphertext)
    decrypted_text, found_key = breaker.break_cypher()

    # 4. Chave Encontrada
    print("Chave Encontrada pelo Algoritmo:")
    print(f"{found_key}")

    # 5. Texto Decifrado
    print(f"\nTexto Decifrado com o Algoritmo:\n{decrypted_text[:100]}...")


if __name__ == "__main__":
    # test_substitution_cipher()
    # test_permutation_cipher()
    substitution_breaker = SubstitutionCypher(
        "Cbobobtbsfzfmmpxdpmpsfeuspqjdbmgsvjutxjefmzdpotvnfebspvoeuifxpsmegpsuifjstxffugmbwpsboetpguufyuvsf,Uifzbsfcpsojombshfcvodiftpocbobobusfftboebsflopxoupcfbhsfbutpvsdfpgfofshzboeqpubttjvn:btxfmmbtfttfoujbmwjubnjotgpsuifcpez,Jobeejujpoupcfjohfbufosbxxifosjqf:uifzdbocfvtfejodblft:tnppuijftboewbsjpvtdvmjobszsfdjqft:cfjohbwfstbujmfboeovusjujpvtgppegpsqfpqmfpgbmmljoet"
    )
    print(substitution_breaker.break_cypher())
    permutation_breaker = PermutationCypher(
        "YRIPISEUTNRCHASCOHHCOUMCNEEFDIPASRCECNITEEIRRGYETFRMAIPNTPETPTAECOIOHSORT"
    )
    print(permutation_breaker.break_cypher())
