import time
import requests
import matplotlib.pyplot as plt
import os

output_dir = "graphs"
os.makedirs(output_dir, exist_ok=True)

BASE_URL = "http://localhost:8000/api/search"

def test_time_kmp(word_counts):
    times = []
    for count in word_counts:
        query = " ".join(["secret" for _ in range(count)])
        params = {"pattern": query}
        print(f"Envoi de la requête KMP avec {count} mots : {query}")
        start = time.time()
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            end = time.time()
            times.append(end - start)
            print(f"Réponse reçue en {end - start:.4f} secondes")
        except requests.exceptions.RequestException as e:
            times.append(None)
            print(f"Erreur lors de la requête KMP : {e}")
    return times

def test_time_regex(lengths):
    times = []
    for length in lengths:
        query = "".join(["(secret)" for _ in range(length)])
        params = {"pattern": query}
        print(f"Envoi de la requête Regex avec une longueur de {length} : {query}")
        start = time.time()
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            end = time.time()
            times.append(end - start)
            print(f"Réponse reçue en {end - start:.4f} secondes")
        except requests.exceptions.RequestException as e:
            times.append(None)
            print(f"Erreur lors de la requête Regex : {e}")
    return times


#word_counts = list(range(1, 31))
regex_lengths = list(range(1, 31))

# Mesure des temps
regex_times = test_time_regex(regex_lengths)


plt.figure(figsize=(10, 5))
plt.plot(regex_lengths, regex_times, marker='s', label='Automate DFA', color='r')
plt.xlabel("Longueur de l'expression régulière")
plt.ylabel("Temps d'exécution (s)")
plt.title("Performance de l'automate DFA")
plt.legend()
plt.grid()

dfa_graph_path = os.path.join(output_dir, "performance_dfa_secret.png")
plt.savefig(dfa_graph_path)

plt.show()