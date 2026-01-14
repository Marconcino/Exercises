class Biglietto:
    def __init__(self, id_biglietto, posto):
        self.id_biglietto = id_biglietto
        self.posto = posto
        self.valido = True
        self.codice_qr = f"QR{id_biglietto:04d}"

    def genera_qr(self):
        print(f"Generato QR Code: {self.codice_qr}")
        return self.codice_qr
