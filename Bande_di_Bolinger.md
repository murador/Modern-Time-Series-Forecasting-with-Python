Ecco il codice Python completo e commentato che crea la medesima simulazione (con i cursori per modificare i parametri in tempo reale):

### Codice Python per la Dashboard (Streamlit)

Salva questo codice in un file chiamato `app.py`:

```python
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. Configurazione della pagina
st.set_page_config(page_title="Dashboard Bande di Bollinger", layout="wide")
st.title("Simulatore: Bande di Bollinger e SMA")
st.write("Modifica i parametri nella barra laterale per vedere l'effetto matematico in tempo reale.")

# 2. Sidebar per gli input utente (i cursori)
st.sidebar.header("Parametri del Modello")
sma_period = st.sidebar.slider("Periodo SMA (Giorni)", min_value=5, max_value=50, value=20)
std_dev_mult = st.sidebar.slider("Moltiplicatore Dev. Standard", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
volatility_scale = st.sidebar.slider("Scala Volatilità (%)", min_value=1, max_value=10, value=3) / 100.0

# 3. Generazione dei dati simulati (Random Walk log-normale)
# Fissiamo il seed per avere un grafico stabile durante i ricalcoli, 
# se vuoi che cambi sempre, commenta la riga seguente:
np.random.seed(42) 
days = 100
# Genera rendimenti casuali in base alla volatilità scelta
returns = np.random.normal(loc=0.0005, scale=volatility_scale, size=days)
# Crea il prezzo cumulato partendo da base 100
price = 100 * np.exp(np.cumsum(returns)) 

df = pd.DataFrame({'Giorno': range(1, days + 1), 'Prezzo': price})

# 4. Calcolo della Matematica (SMA e Bande)
df['SMA'] = df['Prezzo'].rolling(window=sma_period).mean()
df['Std_Dev'] = df['Prezzo'].rolling(window=sma_period).std()

df['Banda_Superiore'] = df['SMA'] + (std_dev_mult * df['Std_Dev'])
df['Banda_Inferiore'] = df['SMA'] - (std_dev_mult * df['Std_Dev'])

# Calcolo della metrica di Squeeze (Larghezza del canale)
df['Band_Width'] = df['Banda_Superiore'] - df['Banda_Inferiore']
current_width = df['Band_Width'].iloc[-1]

# 5. Visualizzazione Metriche
st.metric(
    label="Larghezza Attuale delle Bande (Squeeze Metric)", 
    value=f"{current_width:.2f} punti"
)

# 6. Creazione del grafico interattivo (Plotly)
fig = go.Figure()

# Aggiunta Banda Superiore
fig.add_trace(go.Scatter(
    x=df['Giorno'], y=df['Banda_Superiore'], 
    mode='lines', name='Banda Superiore', 
    line=dict(color='rgba(173, 216, 230, 0.8)', width=1)
))

# Aggiunta Banda Inferiore con riempimento (fill)
fig.add_trace(go.Scatter(
    x=df['Giorno'], y=df['Banda_Inferiore'], 
    mode='lines', name='Banda Inferiore', 
    line=dict(color='rgba(173, 216, 230, 0.8)', width=1),
    fill='tonexty', fillcolor='rgba(173, 216, 230, 0.2)'
))

# Aggiunta SMA (Linea tratteggiata centrale)
fig.add_trace(go.Scatter(
    x=df['Giorno'], y=df['SMA'], 
    mode='lines', name=f'SMA a {sma_period} giorni', 
    line=dict(color='orange', width=2, dash='dash')
))

# Aggiunta Prezzo Simulato
fig.add_trace(go.Scatter(
    x=df['Giorno'], y=df['Prezzo'], 
    mode='lines', name='Prezzo Asset', 
    line=dict(color='blue', width=2)
))

fig.update_layout(
    title="Dinamica dei Prezzi nel Canale di Volatilità",
    xaxis_title="Giorni di Trading",
    yaxis_title="Valore Indice",
    template="plotly_white",
    hovermode="x unified"
)

# Renderizza il grafico sulla dashboard
st.plotly_chart(fig, use_container_width=True)

```

### Come eseguirla sul tuo PC

Per far girare questo codice ti basteranno tre semplici passaggi nel terminale del tuo computer:

1. **Installa le librerie necessarie:**
Copia e incolla nel terminale questo comando:
```bash
pip install streamlit pandas numpy plotly

```


2. **Esegui l'applicazione:**
Spostati nella cartella dove hai salvato il file `app.py` e lancia il comando:
```bash
streamlit run app.py

```


3. Si aprirà automaticamente una nuova scheda nel tuo browser (solitamente all'indirizzo `http://localhost:8501`) con la dashboard perfettamente funzionante. Potrai muovere i cursori a sinistra e vedere il grafico ricalcolare istantaneamente le equazioni di cui abbiamo parlato.

Ottima idea! Usare un ambiente virtuale (Virtual Environment o `venv`) è la *best practice* assoluta in Python. Ti permette di creare una "bolla" isolata per ogni progetto, evitando che le versioni delle librerie vadano in conflitto con altri programmi sul tuo computer.

Ecco la guida passo-passo per preparare il tuo ambiente isolato e far girare la dashboard in totale pulizia.

### 1. Crea la cartella del progetto

Per prima cosa, apri il terminale (Prompt dei Comandi o PowerShell su Windows, Terminale su macOS/Linux) e crea una cartella dedicata al tuo progetto, per poi entrarci.

```bash
mkdir dashboard_finanza
cd dashboard_finanza

```

*Assicurati di salvare il file `app.py` contenente il codice all'interno di questa nuova cartella.*

---

### 2. Crea l'ambiente virtuale

Una volta dentro la cartella del progetto, chiedi a Python di generare un nuovo ambiente virtuale. Per convenzione, la cartella che lo conterrà viene chiamata a sua volta `venv` o `env`.

```bash
python -m venv venv

```

*Nota: Se usi macOS o Linux e il sistema non riconosce `python`, usa `python3 -m venv venv`.*

---

### 3. Attiva l'ambiente virtuale

L'ambiente è stato creato, ma ora devi "entrarci". Il comando per attivarlo cambia in base al tuo sistema operativo:

* **Su Windows:**
```cmd
venv\Scripts\activate

```


* **Su macOS e Linux:**
```bash
source venv/bin/activate

```



> **Come capire se ha funzionato?** Saprai di essere dentro l'ambiente isolato perché all'inizio della riga del tuo terminale comparirà il nome dell'ambiente tra parentesi, in questo modo: `(venv) utente@computer:~/dashboard_finanza$`.

---

### 4. Installa le librerie nella bolla

Ora che l'ambiente è attivo, puoi scaricare le dipendenze. Tutto ciò che installi ora rimarrà rigorosamente confinato all'interno della cartella `venv`, lasciando immacolato il tuo Python di sistema.

```bash
pip install streamlit pandas numpy plotly

```

---

### 5. Avvia la Dashboard

Terminata l'installazione, puoi lanciare l'applicazione esattamente come faresti di solito:

```bash
streamlit run app.py

```

---

### 6. Esci dall'ambiente virtuale (Deactivate)

Quando hai finito di utilizzare l'applicazione e chiudi il server di Streamlit (premendo `Ctrl+C` nel terminale), puoi disattivare l'ambiente virtuale e tornare alla normale configurazione del tuo computer digitando semplicemente:

```bash
deactivate

```

La scritta `(venv)` scomparirà dal terminale. La prossima volta che vorrai riaprire il progetto, non dovrai reinstallare nulla: ti basterà ripetere il **Passaggio 3** per attivare l'ambiente e il **Passaggio 5** per avviare la dashboard!