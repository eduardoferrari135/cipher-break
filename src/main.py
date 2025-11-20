from substitution import SubstitutionCypher
from permutation import PermutationCypher

if __name__ == "__main__":
    # --- Exemplo Substituição ---
    text = SubstitutionCypher.encrypt(
        "By contrast, gradient descent methods can move in any direction that the ridge or alley may ascend or descend. Hence, gradient descent or the conjugate gradient method is generally preferred over hill climbing when the target function is differentiable.",
        "XRIJVLUTBKYHOMSWCAQGZPNEFD",
    )

    substitution_breaker = SubstitutionCypher(text)

    print(substitution_breaker.break_cypher())

    # --- Exemplo Permutação (Seguindo o mesmo padrão) ---
    text_perm = PermutationCypher.encrypt(
        "Encryption works by scrambling data so it is unreadable to unauthorized parties but can be decoded by legitimate users having the correct key.",
        [4, 0, 2, 1, 5, 3],
    )

    permutation_breaker = PermutationCypher(text_perm)

    print(permutation_breaker.break_cypher())