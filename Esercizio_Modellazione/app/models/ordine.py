class OrdineAcquisto:
    def __init__(self, id_ordine, cliente, spettacolo, posto):
        self.id_ordine = id_ordine
        self.cliente = cliente
        self.spettacolo = spettacolo
        self.posto = posto
        self.confermato = False

    def conferma_acquisto(self):
        self.confermato = True
        print("\n ACQUISTO EFFETTUATO CON SUCCESSO! PRONTI A GODERSI LO SPETTACOLO!")
        print(f"Cliente: {self.cliente.nome}")
        print(f"Film: {self.spettacolo.film}")
        print(f"Data: {self.spettacolo.data} {self.spettacolo.ora}")
        print(f"Posti: {', '.join(map(str, self.posto))}")
        print(f"Totale: {self.spettacolo.prezzo * len(self.posto)} €")
