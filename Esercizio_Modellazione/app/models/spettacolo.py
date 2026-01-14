class Spettacolo:
    def __init__(self, id_spettacolo, film, data, ora, prezzo, sala):
        self.id_spettacolo = id_spettacolo
        self.film = film
        self.data = data
        self.ora = ora
        self.prezzo = prezzo
        self.sala = sala

        # Posti dedicati a questo spettacolo
        self.posti_disponibili = list(range(1, sala.posti_totali + 1))

    def mostra_posti(self):
        return self.posti_disponibili

    def occupa_posto(self, posto):
        if posto in self.posti_disponibili:
            self.posti_disponibili.remove(posto)
            return True
        return False
