from models.cliente import Cliente
from models.sala import SalaCinema
from models.spettacolo import Spettacolo
from models.ordine import OrdineAcquisto
from models.pagamento import Pagamento


def main():
    print("Benvenuto al Cinema Lo Spazio \n")

    cliente = Cliente()

    sale = [
        SalaCinema(1, "Sala 1", 10),
        SalaCinema(2, "Sala 2", 8)
    ]

    spettacoli = [
        Spettacolo(1, "Matrix", "2026-01-15", "20:30", 8.50, sale[0]),
        Spettacolo(2, "Avatar 3", "2026-01-16", "21:00", 9.00, sale[1]),
        Spettacolo(3, "Inception", "2026-01-17", "19:30", 7.50, sale[0]),
        Spettacolo(4, "Zootopia 3", "2026-01-18", "19:30", 8.50, sale[0]),
        Spettacolo(5, "Buen Camino", "2026-01-15", "21:30", 8.50, sale[1])
    ]

    # Login / Registrazione
    while not cliente.logged_in:
        scelta = input("Sei registrato? (S/N): ").strip().lower()
        if scelta == "S":
            cliente.login()
        else:
            cliente.registrazione()

    ordine_id = 1
    continua = True

    while continua:
        # Mostra film disponibili
        print("\nFilm disponibili:")
        for s in spettacoli:
            print(f"{s.id_spettacolo}. {s.film} - {s.data} {s.ora} - {s.prezzo} €")

        # Selezione film
        while True:
            try:
                scelta_id = int(input("Seleziona l'ID del film: "))
                spettacolo = next(s for s in spettacoli if s.id_spettacolo == scelta_id)
                break
            except (ValueError, StopIteration):
                print("ID non valido. Riprova.")

        # Numero biglietti
        while True:
            try:
                num_biglietti = int(input(f"\n Quanti biglietti vuoi acquistare? "))
                if 1 <= num_biglietti <= len(spettacolo.mostra_posti()):
                    break
                print("Numero non valido.")
            except ValueError:
                print("Inserisci un numero valido.")

        # Selezione posti
        posti_selezionati = []
        for i in range(num_biglietti):
            while True:
                print(f"\nPosti disponibili ({i+1}/{num_biglietti}): {spettacolo.mostra_posti()}")
                try:
                    posto = int(input(f"Scegli il posto per il biglietto {i+1}: "))
                    if spettacolo.occupa_posto(posto):
                        posti_selezionati.append(posto)
                        break
                    print("Posto non disponibile.")
                except ValueError:
                    print("Inserisci un numero valido.")

        # === CHECKOUT ===
        totale = spettacolo.prezzo * num_biglietti
        pagamento_ok = False

        while not pagamento_ok:
            print(f"\n Totale da pagare: {totale} €")
            print("Metodi di pagamento:")
            for i, metodo in enumerate(Pagamento.METODI, start=1):
                print(f"{i}. {metodo}")

            try:
                scelta = int(input("Seleziona metodo: "))
                metodo = Pagamento.METODI[scelta - 1]
            except (ValueError, IndexError):
                print("Scelta non valida. Riprova.")
                continue

            pagamento = Pagamento(metodo, totale)
            pagamento.inserisci_dati()

            if pagamento.processa_pagamento():
                pagamento_ok = True
                ordine = OrdineAcquisto(
                    ordine_id,
                    cliente,
                    spettacolo,
                    posti_selezionati
                )
                ordine.conferma_acquisto()
                ordine_id += 1
            else:
                print("\n Pagamento fallito. Riprova.")

        # Vuoi fare un altro acquisto?
        cont = input("\n Vuoi acquistare un altro biglietto? (S/N): ").strip().lower()
        if cont != "S":
            continua = False

    print("\n Grazie per aver scelto Cinema Lo Spazio!")


if __name__ == "__main__":
    main()
