class Voiture:
    def __init__(self, num_imma, marque, modele, kilometrage, etat, prix_location):
        self.num_imma = num_imma
        self.marque = marque
        self.modele = modele
        self.kilometrage = kilometrage
        self.etat = etat
        self.prix_location = prix_location
    
    def __str__(self):
        return f'{self.num_imma}, {self.marque}, {self.modele}, {self.kilometrage}, {self.etat}, {self.prix_location}'