import random

class Pagamento:
    METODI = ["Carta", "PayPal", "Klarna", "Satispay"]

    def __init__(self, metodo, importo):
        self.metodo = metodo
        self.importo = importo

    def inserisci_dati(self):
        print(f"\nMetodo selezionato: {self.metodo}")

        if self.metodo == "Carta":
            input("Numero carta: ")
            input("Scadenza (MM/AA): ")
            input("CVV: ")

        elif self.metodo == "PayPal":
            input("Email PayPal: ")

        elif self.metodo == "Klarna":
            input("Email: ")
            input("Data di nascita (GG/MM/AAAA): ")

        elif self.metodo == "Satispay":
            input("Numero di telefono: ")

    def processa_pagamento(self):
        print("\nElaborazione pagamento...")
        # Simulazione esito (80% successo)
        return random.random() < 0.8
