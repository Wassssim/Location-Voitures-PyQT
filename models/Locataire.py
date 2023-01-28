class Locataire:
    def __init__(self, id_loc, nom, prenom, adresse):
        self.id_loc = id_loc
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
    
    def __str__(self):
        return f'{self.id_loc}, {self.nom}, {self.prenom}, {self.adresse}'