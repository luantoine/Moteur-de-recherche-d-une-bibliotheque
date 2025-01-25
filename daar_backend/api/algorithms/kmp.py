def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0  # longueur du précédent plus long préfixe suffixe
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    matches = []
    lps = compute_lps(pattern)
    i = j = 0  # index pour text et pattern
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches

def egrep_KMP(pattern, file_path):
    lps = compute_lps(pattern)

    matches = []

    # Parcourir le fichier ligne par ligne
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if kmp_search_avec_lps(line, pattern, lps):
                matches.append((line_num, line))

    return matches

def kmp_search_avec_lps(text, pattern, lps):
    i = j = 0  # index pour text et pattern
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            return True  # Pattern trouvé, on peut arrêter
        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False  # Si le pattern n'a pas été trouvé

def kmp_search_pos(text: str, pattern: str, lps: list):
    """
    Retourne **la liste complète des positions** où 'pattern' apparaît dans 'text',
    grâce à l'algorithme KMP, en réutilisant le tableau 'lps'.
    """
    positions = []
    i, j = 0, 0  # i pour text, j pour pattern
    n, m = len(text), len(pattern)

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            # Pattern trouvé
            if j == m:
                positions.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions

def main():
    pattern = "abc"
    text = "ababcabcababc"
    matches = kmp_search(text, pattern)
    for index in matches:
        print(f"Correspondance trouvée à la position {index}")

if __name__ == "__main__":
    main()
