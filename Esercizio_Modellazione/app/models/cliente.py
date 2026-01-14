class Cliente:
    def __init__(self):
        self.nome = None
        self.password = None
        self.logged_in = False

    def registrazione(self):
        self.nome = input("Inserisci il tuo nome: ").strip()
        self.password = input("Crea la tua password: ").strip()

        print(f"\nRegistrazione completata per {self.nome}")
        self.logged_in = True
        return self.logged_in

    def login(self):
        nome = input("Nome: ").strip()
        password = input("Password: ").strip()

        if nome == self.nome and password == self.password:
            print("Login effettuato con successo")
            self.logged_in = True
            return True
        else:
            print("Nome o password errati")
            return False
