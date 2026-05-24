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
