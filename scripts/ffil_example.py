import numpy as np
import pandas as pd

index = pd.to_datetime([
	'2023-01-02', '2023-01-03', '2023-01-04',
	'2023-01-05', '2023-01-06'
])

s = pd.Series([100, 101, np.nan, 103, 104], index=index)
print("Originale:")
print(s)

# Forward fill: sostituisce NaN con l'ultimo valore valido precedente
filled = s.ffill()
print("\nDopo ffill():")
print(filled)

# Alternativa in-place
s2 = pd.Series([100, 101, np.nan, 103, 104], index=index)
s2.ffill(inplace=True)
print("\nEsempio in-place:")
print(s2)

"""
Forward Fill Example
Originale:
2023-01-02    100.0
2023-01-03    101.0
2023-01-04      NaN
2023-01-05    103.0
2023-01-06    104.0
dtype: float64

Dopo ffill():
2023-01-02    100.0
2023-01-03    101.0
2023-01-04    101.0
2023-01-05    103.0
2023-01-06    104.0
dtype: float64

Esempio in-place:
2023-01-02    100.0
2023-01-03    101.0
2023-01-04    101.0
2023-01-05    103.0
2023-01-06    104.0
dtype: float64s

"""