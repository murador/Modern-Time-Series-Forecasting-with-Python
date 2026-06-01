"""statistica_descrittiva.py

Scarica i prezzi adjusted close da Yahoo Finance per i titoli
AAPL, MSFT, AMZN, GOOG, META, TSLA, NVDA, JPM, V, BAC nel periodo
2010-01-01 - 2023-12-31 e calcola la matrice di correlazione tra
i rendimenti giornalieri.

Output:
- `corr_matrix.csv` : matrice di correlazione (CSV)
- `corr_heatmap.png` : heatmap (se `seaborn` e `matplotlib` sono disponibili)
"""

import os  # import del modulo os per eventuali operazioni di file
from typing import List  # typing per annotazioni dei tipi

import pandas as pd  # import pandas come pd per gestire DataFrame


TICKERS: List[str] = [  # lista dei simboli da scaricare
	"AAPL",  # Apple
	"MSFT",  # Microsoft
	"AMZN",  # Amazon
	"GOOG",  # Google
	"META",  # Meta (Facebook)
	"TSLA",  # Tesla
	"NVDA",  # Nvidia
	"JPM",  # JP Morgan
	"V",  # Visa
	"BAC",  # Bank of America
]

START = "2010-01-01"  # data di inizio (YYYY-MM-DD)
END = "2023-12-31"  # data di fine (YYYY-MM-DD)


def download_adj_close(tickers: List[str], start: str, end: str) -> pd.DataFrame:  # funzione per scaricare prezzi adjusted
	try:
		import yfinance as yf  # import locale di yfinance
	except Exception as e:
		raise ImportError("yfinance non è installato. Esegui: pip install yfinance") from e  # errore se manca yfinance

	data = yf.download(tickers, start=start, end=end, progress=False)  # scarica i dati con yfinance

	# Prova diverse modalità per estrarre 'Adj Close' perché yfinance
	# può restituire colonne a singolo livello, MultiIndex con attributi
	# come primo livello o ticker come primo livello, oppure già un DataFrame
	# contenente solo gli adjusted close.
	def _extract_adj(df: pd.DataFrame) -> pd.DataFrame:  # helper per estrarre 'Adj Close'
		# caso: colonne a livello singolo dove 'Adj Close' è il nome della colonna
		# Adj Close è il prezzo di chiusura aggiustato per dividendi e frazionamenti, più accurato per analisi di rendimento
		if "Adj Close" in df.columns:
			adj = df["Adj Close"]  # prendi la colonna 'Adj Close'
			if isinstance(adj, pd.Series):
				adj = adj.to_frame(name=tickers[0])  # se è Series, trasformala in DataFrame
			return adj  # ritorna adjusted close

		# caso: colonne MultiIndex
		if isinstance(df.columns, pd.MultiIndex):
			# prova livello 0
			if "Adj Close" in df.columns.get_level_values(0):
				adj = df["Adj Close"]  # estrai livello 'Adj Close'
				if isinstance(adj, pd.Series):
					adj = adj.to_frame(name=tickers[0])  # normalizza a DataFrame
				return adj  # ritorna adjusted close

			# prova livello 1
			if df.columns.nlevels > 1 and "Adj Close" in df.columns.get_level_values(1):
				adj = df.xs("Adj Close", axis=1, level=1)  # prendi cross-section level=1
				return adj  # ritorna adjusted close

			# prova il pattern con tickers come livello superiore e attributi come secondo livello
			try:
				cols = []  # lista temporanea di colonne trovate
				for t in tickers:
					if (t, "Adj Close") in df.columns:  # verifica presenza tupla (ticker, 'Adj Close')
						cols.append((t, "Adj Close"))  # aggiungi alla lista
				if cols:
					adj = df.loc[:, cols]  # seleziona solo quelle colonne
					# flatten columns to ticker names
					adj.columns = [c[0] for c in adj.columns]  # semplifica Intestazioni a solo ticker
					return adj  # ritorna adjusted close
			except Exception:
				pass  # ignora eccezioni in questo tentativo

		# caso: i dati scaricati contengono già solo adjusted close (colonne = tickers)
		if set(df.columns).intersection(set(tickers)):
			possible = [c for c in df.columns if c in tickers]  # filtra colonne che sono tickers
			return df[possible]  # ritorna DataFrame con colonne ticker

		# nessun caso corrispondente
		# prova fallback su 'Close' se 'Adj Close' non è disponibile
		if "Close" in df.columns or (
			isinstance(df.columns, pd.MultiIndex)
			and ("Close" in df.columns.get_level_values(0) or (df.columns.nlevels > 1 and "Close" in df.columns.get_level_values(1)))
		):
			try:
				if "Close" in df.columns:
					close = df["Close"]  # usa 'Close' come fallback
					if isinstance(close, pd.Series):
						close = close.to_frame(name=tickers[0])  # normalizza a DataFrame
					return close  # ritorna close
				if isinstance(df.columns, pd.MultiIndex) and df.columns.nlevels > 1 and "Close" in df.columns.get_level_values(1):
					close = df.xs("Close", axis=1, level=1)  # xs per level 'Close'
					return close  # ritorna close
			except Exception:
				pass  # ignora errori nel fallback

		# nessun caso corrispondente - output diagnostico
		print("DEBUG: yfinance ha restituito colonne inattese:")  # debug colonne
		print(list(df.columns))  # stampa lista colonne
		try:
			print(df.head(3))  # stampa le prime 3 righe per diagnostica
		except Exception:
			pass  # ignora se non stampabile
		raise KeyError(
			"Adj Close non trovato. Controlla l'output di yfinance (vedi debug sopra)."
		)  # solleva errore esplicito

	adj_close = _extract_adj(data)  # usa helper per estrarre adjusted close
	# drop rows where all tickers are NaN
	adj_close = adj_close.dropna(how="all")  # rimuovi righe vuote
	return adj_close  # ritorna DataFrame di prezzi adjusted


def daily_returns(adj_close: pd.DataFrame) -> pd.DataFrame:  # calcola rendimenti giornalieri
	returns = adj_close.pct_change().dropna(how="all")  # pct_change e rimuovi prime NaN
	return returns  # ritorna DataFrame dei rendimenti


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:  # calcola matrice di correlazione
	return returns.corr()  # usa metodo corr di pandas


def save_corr(corr: pd.DataFrame, filepath: str = "corr_matrix.csv") -> None:  # salva CSV
	corr.to_csv(filepath)  # scrive su file CSV


def plot_heatmap(corr: pd.DataFrame, filepath: str = "corr_heatmap.png") -> None:  # disegna heatmap
	try:
		import matplotlib.pyplot as plt  # import matplotlib
		import seaborn as sns  # import seaborn
	except Exception:
		print("Seaborn/matplotlib non installati: salto la generazione della heatmap.")  # avviso se mancanti
		return  # esci se non disponibili

	plt.figure(figsize=(10, 8))  # imposta dimensione figura
	sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)  # disegna heatmap
	plt.title("Correlation matrix - daily returns")  # titolo figura
	plt.tight_layout()  # layout tighter
	plt.savefig(filepath)  # salva immagine
	plt.close()  # chiudi figura


def main() -> None:  # funzione principale
	adj = download_adj_close(TICKERS, START, END)  # scarica prezzi adjusted
	returns = daily_returns(adj)  # calcola rendimenti giornalieri
	corr = correlation_matrix(returns)  # calcola matrice di correlazione

	print("Matrice di correlazione (preview):")  # stampa anteprima
	print(corr)  # stampa matrice

	save_corr(corr, "corr_matrix.csv")  # salva CSV
	plot_heatmap(corr, "corr_heatmap.png")  # genera heatmap opzionale

	print("File salvati: corr_matrix.csv e corr_heatmap.png (se disponibile).")  # conferma salvataggio


if __name__ == "__main__":  # entrypoint script
	main()  # esegui main
