#!/usr/bin/env python3
"""
Esempio semplice di calcolo del Net Present Value (NPV)
e dell'Internal Rate of Return (IRR) usando numpy_financial.

Installazione:
    pip install numpy-financial

Esecuzione:
    python scripts/financial_examples.py
"""

import numpy_financial as nf


def example_npv_irr():
    # Tasso di sconto (10%)
    rate = 0.10

    # Flussi di cassa: investimento iniziale negativo seguito dai ritorni
    cashflows = [-1000, 300, 420, 680]

    # Calcolo del NPV: numpy_financial.npv sconta i flussi a partire da t=0
    npv = nf.npv(rate, cashflows)

    # Calcolo del IRR: restituisce il tasso che azzera il NPV
    irr = nf.irr(cashflows)

    # Spiegazione (esempio):
    # - NPV (Net Present Value / Valore Attuale Netto): è la somma dei flussi di cassa
    #   futuri attualizzati al tasso di sconto scelto, meno l'investimento iniziale.
    #   In questo esempio il NPV è calcolato scontando i flussi al 10%.
    #   Un NPV positivo (es. NPV = 130.73) significa che, scontando i flussi al
    #   10%, il progetto genera un valore netto positivo pari a quella cifra.
    #   Economicamente: un NPV positivo indica che il progetto aggiunge valore
    #   rispetto all'alternativa rappresentata dal tasso di sconto (qui 10%).
    #   Se il tasso di sconto rappresenta il costo del capitale, allora il progetto
    #   remunera il capitale e crea valore per gli investitori.

    # - IRR (Internal Rate of Return / Tasso Interno di Rendimento): è il tasso
    #   di sconto che rende il NPV uguale a zero. Rappresenta il rendimento
    #   annualizzato implicito del progetto dato il profilo dei flussi di cassa.
    #   Economicamente: se l'IRR è maggiore del tasso minimo richiesto (hurdle rate)
    #   o del costo del capitale, il progetto è considerato attrattivo.
    #   Ad esempio, nell'output di esempio l'IRR è circa 16.34%:
    #     - Se il nostro requisito fosse il 16%, un IRR di 16.34% significa che il
    #       rendimento atteso del progetto supera leggermente la soglia: il progetto
    #       è quindi marginalmente conveniente rispetto a quella soglia.
    #     - In termini pratici, IRR > 16% indica che il progetto restituirà più del
    #       16% annuo (approssimativamente) e quindi è preferibile rispetto a un
    #       investimento alternativo che offrisse solo il 16%.

    return rate, cashflows, npv, irr


def main():
    rate, cashflows, npv, irr = example_npv_irr()
    # Print dei risultati calcolati
    print(f"Discount rate: {rate:.2%}")
    print(f"Cashflows: {cashflows}")
    print(f"NPV: {npv:.2f}")
    if irr is not None:
        print(f"IRR: {irr:.2%}")
    else:
        print("IRR: non trovata")


# Esempio di output (da includere come commento):
# Discount rate: 10.00%
# Cashflows: [-1000, 300, 420, 680]
# NPV: 130.73
# IRR: 16.34%


if __name__ == "__main__":
    main()
