import numpy as np
import pandas as pd
import time

# Dati di esempio: prezzi e quantità di titoli in portfolio
n_titoli = 10000000
prezzi = np.random.uniform(10, 1000, n_titoli)
quantita = np.random.randint(1, 100, n_titoli)

print("=" * 60)
print("CONFRONTO: NumPy vs Loop Python Classico")
print("=" * 60)
print(f"Numero di titoli nel portfolio: {n_titoli}\n")

# METODO 1: Loop Python Classico
print("1. METODO CON LOOP PYTHON CLASSICO:")
start_time = time.time()
valore_totale_python = 0
for i in range(n_titoli):
    valore_totale_python += prezzi[i] * quantita[i]
end_time = time.time()
tempo_python = end_time - start_time

print(f"   Valore totale portfolio: €{valore_totale_python:,.2f}")
print(f"   Tempo di esecuzione: {tempo_python * 1000:.4f} ms\n")

# METODO 2: NumPy (vettorizzato)
print("2. METODO CON NumPy (vettorizzato):")
start_time = time.time()
valore_totale_numpy = np.sum(prezzi * quantita)
end_time = time.time()
tempo_numpy = end_time - start_time

print(f"   Valore totale portfolio: €{valore_totale_numpy:,.2f}")
print(f"   Tempo di esecuzione: {tempo_numpy * 1000:.4f} ms\n")

# Calcolo del miglioramento
speedup = tempo_python / tempo_numpy
print("=" * 60)
print(f"RISULTATI:")
print(f"   Speedup (NumPy è {speedup:.2f}x più veloce)")
print(f"   Differenza: {(tempo_python - tempo_numpy) * 1000:.4f} ms")
print("=" * 60)

# Tabella con Pandas
print("\n3. RIEPILOGO CON PANDAS:")
dati = {
    'Metodo': ['Loop Python', 'NumPy'],
    'Tempo (ms)': [tempo_python * 1000, tempo_numpy * 1000],
    'Valore Portfolio (€)': [valore_totale_python, valore_totale_numpy]
}
df = pd.DataFrame(dati)
print(df.to_string(index=False))
