"""rendimenti.py

Script per analisi e visualizzazione dei dati azionari (2022-2023)
- Download dei dati `Adj Close` per AAPL, MSFT, GOOG, SPY tramite yfinance
- Grafico a linee del prezzo di AAPL
- Calcolo dei rendimenti giornalieri per tutti i titoli
- Istogramma dei rendimenti giornalieri di AAPL con KDE e linea della media

Commenti in italiano per spiegare i passaggi.
"""

# import principali
try:
    import yfinance as yf  # libreria per scaricare dati finanziari
except Exception as e:
    raise ImportError("yfinance non è installato. Esegui: pip install yfinance") from e

import pandas as pd  # gestione dati tabulari
import matplotlib.pyplot as plt  # plotting
import seaborn as sns  # visualizzazioni statistiche

# Parametri principali
TICKERS = ["AAPL", "MSFT", "GOOG", "SPY"]  # lista dei ticker da analizzare
START = "2022-01-01"  # data di inizio
END = "2023-12-31"  # data di fine

# Impostazione stile Matplotlib/Seaborn
plt.style.use("seaborn-v0_8-whitegrid")  # stile grafici coerente
sns.set_theme(style="whitegrid")  # tema seaborn


def download_adj_close(tickers, start, end):
    """Scarica i prezzi adjusted close per i ticker richiesti.

    Gestisce possibili formati di output di yfinance (MultiIndex o colonne singole).
    Restituisce un DataFrame con colonne pari ai ticker e indice su datetime.
    """
    data = yf.download(tickers, start=start, end=end, progress=False)

    # Helper per estrarre adjusted close in modo robusto
    def _extract_adj(df: pd.DataFrame) -> pd.DataFrame:
        # caso: colonne a livello singolo con 'Adj Close'
        if "Adj Close" in df.columns:
            adj = df["Adj Close"]
            if isinstance(adj, pd.Series):
                adj = adj.to_frame(name=tickers[0])
            return adj

        # caso: colonne MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            # prova livello 0
            if "Adj Close" in df.columns.get_level_values(0):
                adj = df["Adj Close"]
                if isinstance(adj, pd.Series):
                    adj = adj.to_frame(name=tickers[0])
                return adj

            # prova livello 1
            if df.columns.nlevels > 1 and "Adj Close" in df.columns.get_level_values(1):
                adj = df.xs("Adj Close", axis=1, level=1)
                return adj

            # prova pattern (ticker, 'Adj Close')
            try:
                cols = []
                for t in tickers:
                    if (t, "Adj Close") in df.columns:
                        cols.append((t, "Adj Close"))
                if cols:
                    adj = df.loc[:, cols]
                    adj.columns = [c[0] for c in adj.columns]
                    return adj
            except Exception:
                pass

        # caso: il DataFrame ha già colonne pari ai ticker
        if set(df.columns).intersection(set(tickers)):
            possible = [c for c in df.columns if c in tickers]
            return df[possible]

        # fallback: prova con 'Close' se 'Adj Close' non è disponibile
        if "Close" in df.columns or (
            isinstance(df.columns, pd.MultiIndex)
            and ("Close" in df.columns.get_level_values(0) or (df.columns.nlevels > 1 and "Close" in df.columns.get_level_values(1)))
        ):
            try:
                if "Close" in df.columns:
                    close = df["Close"]
                    if isinstance(close, pd.Series):
                        close = close.to_frame(name=tickers[0])
                    return close
                if isinstance(df.columns, pd.MultiIndex) and df.columns.nlevels > 1 and "Close" in df.columns.get_level_values(1):
                    close = df.xs("Close", axis=1, level=1)
                    return close
            except Exception:
                pass

        # diagnostica
        print("DEBUG: yfinance ha restituito colonne inattese:", list(df.columns))
        try:
            print(df.head(3))
        except Exception:
            pass
        raise KeyError("Adj Close non trovato nell'output di yfinance")

    adj = _extract_adj(data)

    # Se il risultato è una Series (es. un solo ticker), trasformalo in DataFrame
    if isinstance(adj, pd.Series):
        adj = adj.to_frame(name=tickers[0])

    # Assicuriamoci che l'indice sia datetime e ordinato
    adj.index = pd.to_datetime(adj.index)
    adj = adj.sort_index()

    return adj


def plot_aapl_price(adj_df, savepath=None):
    """Grafico a linee del prezzo adjusted close di AAPL.

    Parametri:
    - adj_df: DataFrame con colonne ticker
    - savepath: se fornito, salva la figura su file
    """
    if "AAPL" not in adj_df.columns:
        raise KeyError("AAPL non presente nei dati scaricati")

    # Estrai la serie di AAPL
    aapl = adj_df["AAPL"]

    # Crea figura
    plt.figure(figsize=(12, 6))
    plt.plot(aapl.index, aapl.values, label="AAPL", color="#1f77b4")  # linea dei prezzi
    plt.title("AAPL - Prezzo di Chiusura Rettificato (2022-2023)")  # titolo
    plt.xlabel("Data")  # etichetta asse x
    plt.ylabel("Prezzo di Chiusura Rettificato (USD)")  # etichetta asse y
    plt.legend()  # legenda
    plt.grid(True)  # griglia
    plt.tight_layout()

    if savepath:
        plt.savefig(savepath, dpi=300)  # salva la figura

    plt.show()  # mostra il grafico


def compute_daily_returns(adj_df):
    """Calcola i rendimenti giornalieri (pct_change) per tutti i ticker.

    Restituisce un DataFrame di rendimenti (drop delle righe NaN iniziali).
    pct_change calcola la variazione percentuale
    tra i prezzi di chiusura rettificati di giorni consecutivi.
    ad esempio, se il prezzo di AAPL il giorno t è 150 e 
    il giorno t+1 è 153,
    il rendimento giornaliero sarà (153-150)/150 = 0.02 = 2%. 
    """
    returns = adj_df.pct_change()  # variazione percentuale giornaliera
    returns = returns.dropna(how="all")  # rimuovi righe con tutti NaN
    return returns


def plot_aapl_returns_hist(returns_df, bins=50, savepath=None):
    """Disegna istogramma dei rendimenti giornalieri di AAPL con KDE e linea della media."""
    if "AAPL" not in returns_df.columns:
        raise KeyError("AAPL non presente nei rendimenti calcolati")

    aapl_ret = returns_df["AAPL"].dropna()

    plt.figure(figsize=(10, 6))
    sns.histplot(aapl_ret, bins=bins, kde=True, stat="density", color="#2ca02c")

    # linea verticale per la media
    mean_val = aapl_ret.mean()
    plt.axvline(mean_val, color="red", linestyle="--", linewidth=2, label=f"Media = {mean_val:.5f}")

    plt.title("Istogramma dei rendimenti giornalieri di AAPL (2022-2023)")
    plt.xlabel("Rendimento giornaliero")
    plt.ylabel("Densità")
    plt.legend()
    plt.tight_layout()

    if savepath:
        plt.savefig(savepath, dpi=300)

    plt.show()


def main():
    # Scarica i dati adjusted close
    adj = download_adj_close(TICKERS, START, END)

    # Grafico prezzo AAPL
    plot_aapl_price(adj, savepath="AAPL_price_2022_2023.png")

    # Calcola rendimenti giornalieri
    returns = compute_daily_returns(adj)

    # Istogramma dei rendimenti AAPL
    plot_aapl_returns_hist(returns, bins=50, savepath="AAPL_returns_hist.png")


if __name__ == "__main__":
    main()
