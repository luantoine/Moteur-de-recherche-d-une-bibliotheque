import time
import requests
import matplotlib.pyplot as plt
import os

output_dir = "graphs"
os.makedirs(output_dir, exist_ok=True)

BASE_URL = "http://localhost:8000/api/search"

kmp_test = [
    "aaa aaa aaa",
    "a b c d e f",
    "machine learning algorithm",
    "azerty quiop"
]

regex_test = [
    "(a|b|c|d|e|f)",
    "(an)*",
    "((a|b)(n|m))*",
    "(secret|santa|white|elephant)"
]

def test_kmp(queries):
    times = []
    for query in queries:
        params = {"pattern": query}
        print(f"Test KMP avec '{query}'")
        start = time.time()
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            end = time.time()
            times.append(end - start)
            print(f"Réponse en {end - start:.4f} sec")
        except requests.exceptions.RequestException as e:
            times.append(None)
            print(f"Erreur KMP {e}")
    return times

def test_regex(queries):
    times = []
    for query in queries:
        params = {"pattern": query}
        print(f"Test Regex avec '{query}'")
        start = time.time()
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            end = time.time()
            times.append(end - start)
            print(f"Réponse en {end - start:.4f} sec")
        except requests.exceptions.RequestException as e:
            times.append(None)
            print(f"Erreur Regex {e}")
    return times

kmp_times = test_kmp(kmp_test)
regex_times = test_regex(regex_test)

plt.figure(figsize=(12, 6))
x_labels = kmp_test + regex_test
x_positions = range(len(x_labels))

plt.bar(x_positions[:len(kmp_test)], kmp_times, color='b', alpha=0.7, label='KMP')
plt.bar(x_positions[len(kmp_test):], regex_times, color='r', alpha=0.7, label='Regex')

plt.xticks(x_positions, x_labels, rotation=45, ha="right")
plt.xlabel("Type de requête")
plt.ylabel("Temps d'exécution (s)")
plt.title("Performance des requêtes spéciales")
plt.legend()
plt.grid()

graph_path = os.path.join(output_dir, "performance_special_cases.png")
plt.savefig(graph_path)
plt.show()
