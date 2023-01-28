import sys
import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel
from models.Voiture import Voiture
from models.Locataire import Locataire

DB_PATH = ".\\location_voiture.db"

class DBConnector():
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        print(self.connection.total_changes)

    def getVoitures(self):
        cursor = self.connection.cursor()
        rows = cursor.execute("SELECT * FROM voiture").fetchall()
        return rows

    def addVoiture(self, voiture):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO voiture VALUES ('{voiture.num_imma}', '{voiture.marque}', '{voiture.modele}', '{voiture.kilometrage}', '{voiture.etat}', '{voiture.prix_location}')")
        self.connection.commit()
    
    def updateVoiture(self, voiture):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE voiture SET marque = ? , modele = ? , kilometrage = ? , etat = ? , prix_location = ? WHERE num_imma = ?",
            (voiture.marque, voiture.modele, voiture.kilometrage, voiture.etat, voiture.prix_location, voiture.num_imma)
        )
        self.connection.commit()
    
    def deleteVoiture(self, num_imma):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM voiture WHERE num_imma = '{num_imma}'")
        self.connection.commit()
        
    def getLocataires(self):
        cursor = self.connection.cursor()
        rows = cursor.execute("SELECT * FROM locataire").fetchall()
        return rows
    
    def addLocataire(self, locataire):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO locataire VALUES ('{locataire.id_loc}', '{locataire.nom}', '{locataire.prenom}', '{locataire.adresse}')")
        self.connection.commit()
    
    def updateLocataire(self, locataire):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE locataire SET nom = ? , prenom = ? , adresse = ? WHERE id_loc = ?",
            (locataire.nom, locataire.prenom, locataire.adresse, locataire.id_loc)
        )
        self.connection.commit()
        
    def deleteLocataire(self, id_loc):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM locataire WHERE id_loc = '{id_loc}'")
        self.connection.commit()

        
class MainWindow(QMainWindow):
    def __init__(self, dbConnector):
        super().__init__()
        self.setWindowTitle("Gestion de location de voitures")
        self.setGeometry(100, 100, 800, 600)

        # connecteur de la bd
        self.dbConnector = dbConnector
        
        # collections d'objets de voitures et locataires
        self.voitures = []
        self.locataires = []

        # widgets pour la gestion des voitures
        self.voitures_table = QTableWidget()
        self.voitures_table.setColumnCount(6)
        self.voitures_table.setHorizontalHeaderLabels(["Num_imma", "Marque", "Modele", "Kilometrage", "Etat", "Prix_location"])
        self.voitures_table.cellChanged.connect(self.modify_voiture)
        self.delete_voiture_btn = QPushButton("Supprimer une voiture")
        self.delete_voiture_btn.clicked.connect(self.delete_voiture)
        
        # widgets pour la formulaire d'ajout de voiture
        self.add_voiture_form = QWidget()
        self.add_voiture_form_layout = QVBoxLayout()
        self.add_voiture_form.setLayout(self.add_voiture_form_layout)
        self.add_voiture_form_label = QLabel("Ajouter une voiture")
        self.add_voiture_form_num_imma_input = QLineEdit()
        self.add_voiture_form_num_imma_input.setPlaceholderText("Numéro d'immatriculation")
        self.add_voiture_form_marque_input = QLineEdit()
        self.add_voiture_form_marque_input.setPlaceholderText("Marque")
        self.add_voiture_form_modele_input = QLineEdit()
        self.add_voiture_form_modele_input.setPlaceholderText("Modèle")
        self.add_voiture_form_kilometrage_input = QLineEdit()
        self.add_voiture_form_kilometrage_input.setPlaceholderText("Kilométrage")
        self.add_voiture_form_etat_input = QLineEdit()
        self.add_voiture_form_etat_input.setPlaceholderText("Etat")
        self.add_voiture_form_prix_location_input = QLineEdit()
        self.add_voiture_form_prix_location_input.setPlaceholderText("Prix de location")
        self.add_voiture_form_submit_btn = QPushButton("Ajouter")
        self.add_voiture_form_submit_btn.clicked.connect(self.add_voiture)
        self.add_voiture_form_layout.addWidget(self.add_voiture_form_label)
        self.add_voiture_form_layout.addWidget(self.add_voiture_form_num_imma_input)
        self.add_voiture_form_layout.addWidget(self.add_voiture_form_marque_input)
        self.add_voiture_form_layout.addWidget(self.add_voiture_form_modele_input)
        self.add_voiture_form_layout.addWidget(self.add_voiture_form_kilometrage_input)
        self.add_voiture_form_layout.addWidget(self.add_voiture_form_etat_input)
        self.add_voiture_form_layout.addWidget(self.add_voiture_form_prix_location_input)
        self.add_voiture_form_layout.addWidget(self.add_voiture_form_submit_btn)
        

        # widgets pour la gestion des locataires
        self.locataires_table = QTableWidget()
        self.locataires_table.setColumnCount(4)
        self.locataires_table.setHorizontalHeaderLabels(["Id_loc", "Nom", "Prenom", "Adresse"])
        self.locataires_table.cellChanged.connect(self.modify_locataire)
        self.delete_locataire_btn = QPushButton("Supprimer un locataire")
        self.delete_locataire_btn.clicked.connect(self.delete_locataire)
        self.search_locataire_btn = QPushButton("Rechercher un locataire")
        self.search_locataire_btn.clicked.connect(self.search_locataire)
        self.locataire_search_input = QLineEdit()
        self.locataire_search_input.setPlaceholderText("Entrez l'ID ou le nom du locataire")
        
        # widgets pour la formulaire d'ajout d'un locataire
        self.add_locataire_form = QWidget()
        self.add_locataire_form_layout = QVBoxLayout()
        self.add_locataire_form.setLayout(self.add_locataire_form_layout)
        self.add_locataire_form_label = QLabel("Ajouter un locataire")
        self.add_locataire_form_id_loc_input = QLineEdit()
        self.add_locataire_form_id_loc_input.setPlaceholderText("ID du locataire")
        self.add_locataire_form_nom_input = QLineEdit()
        self.add_locataire_form_nom_input.setPlaceholderText("Nom")
        self.add_locataire_form_prenom_input = QLineEdit()
        self.add_locataire_form_prenom_input.setPlaceholderText("Prénom")
        self.add_locataire_form_adresse_input = QLineEdit()
        self.add_locataire_form_adresse_input.setPlaceholderText("Adresse")
        self.add_locataire_form_submit_btn = QPushButton("Ajouter")
        self.add_locataire_form_submit_btn.clicked.connect(self.add_locataire)
        self.add_locataire_form_layout.addWidget(self.add_locataire_form_label)
        self.add_locataire_form_layout.addWidget(self.add_locataire_form_id_loc_input)
        self.add_locataire_form_layout.addWidget(self.add_locataire_form_nom_input)
        self.add_locataire_form_layout.addWidget(self.add_locataire_form_prenom_input)
        self.add_locataire_form_layout.addWidget(self.add_locataire_form_adresse_input)
        self.add_locataire_form_layout.addWidget(self.add_locataire_form_submit_btn)
        

        # widgets pour la gestion des locations
        self.louer_voiture_btn = QPushButton("Louer une voiture")
        self.louer_voiture_btn.clicked.connect(self.louer_voiture)
        self.rendre_voiture_btn = QPushButton("Rendre une voiture")
        self.rendre_voiture_btn.clicked.connect(self.rendre_voiture)
        self.location_table = QTableWidget()
        self.location_table.setColumnCount(7)
        self.location_table.setHorizontalHeaderLabels(["Num_imma", "Marque", "Modele", "Kilometrage", "Etat", "Prix_location", "Locataire"])
        
        # layout principal
        self.mainWidget = QWidget()
        self.main_layout = QVBoxLayout()
        self.mainWidget.setLayout(self.main_layout)
        self.setCentralWidget(self.mainWidget)

        # layout pour la gestion des voitures
        self.voitures_layout = QHBoxLayout()
        self.voitures_layout.addWidget(self.add_voiture_form, 2)
        self.voitures_layout.addWidget(self.voitures_table, 10)
        self.voitures_layout.addWidget(self.delete_voiture_btn, 1)

        # layout pour la gestion des locataires
        self.locataires_layout = QHBoxLayout()
        self.locataires_layout.addWidget(self.add_locataire_form, 2)
        self.locataires_layout.addWidget(self.locataires_table, 15)
        self.locataires_layout.addWidget(self.delete_locataire_btn, 1)
        self.locataires_layout.addWidget(self.search_locataire_btn, 1)
        self.locataires_layout.addWidget(self.locataire_search_input, 1)

        # layout pour la gestion des locations
        self.location_layout = QHBoxLayout()
        self.location_layout.addWidget(self.location_table)
        self.location_layout.addWidget(self.louer_voiture_btn)
        self.location_layout.addWidget(self.rendre_voiture_btn)

        # ajout des layouts à la fenêtre principale
        self.main_layout.addLayout(self.voitures_layout)
        self.main_layout.addLayout(self.locataires_layout)
        self.main_layout.addLayout(self.location_layout)
        
        # initializer les données
        self.init_voitures(dbConnector.getVoitures())
        self.init_locataires(dbConnector.getLocataires())

    def init_voitures(self, rows):
        for row in rows:
            self.voitures.append(
                Voiture(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )
            
            rowPosition = self.voitures_table.rowCount()
            self.voitures_table.insertRow(rowPosition)
            self.voitures_table.setItem(rowPosition , 0, QTableWidgetItem(self.voitures[-1].num_imma))
            self.voitures_table.setItem(rowPosition , 1, QTableWidgetItem(self.voitures[-1].marque))
            self.voitures_table.setItem(rowPosition , 2, QTableWidgetItem(self.voitures[-1].modele))
            self.voitures_table.setItem(rowPosition , 3, QTableWidgetItem(self.voitures[-1].kilometrage))
            self.voitures_table.setItem(rowPosition , 4, QTableWidgetItem(self.voitures[-1].etat))
            self.voitures_table.setItem(rowPosition , 5, QTableWidgetItem(self.voitures[-1].prix_location))
    
    
    def add_voiture(self):
        self.voitures.append(
            Voiture(
                self.add_voiture_form_num_imma_input.text(),
                self.add_voiture_form_marque_input.text(),
                self.add_voiture_form_modele_input.text(),
                self.add_voiture_form_kilometrage_input.text(),
                self.add_voiture_form_etat_input.text(),
                self.add_voiture_form_prix_location_input.text()
            )
        )
        
        rowPosition = self.voitures_table.rowCount()
        self.voitures_table.insertRow(rowPosition)
        self.voitures_table.setItem(rowPosition , 0, QTableWidgetItem(self.voitures[-1].num_imma))
        self.voitures_table.setItem(rowPosition , 1, QTableWidgetItem(self.voitures[-1].marque))
        self.voitures_table.setItem(rowPosition , 2, QTableWidgetItem(self.voitures[-1].modele))
        self.voitures_table.setItem(rowPosition , 3, QTableWidgetItem(self.voitures[-1].kilometrage))
        self.voitures_table.setItem(rowPosition , 4, QTableWidgetItem(self.voitures[-1].etat))
        self.voitures_table.setItem(rowPosition , 5, QTableWidgetItem(self.voitures[-1].prix_location))
        
        self.dbConnector.addVoiture(self.voitures[-1])
        
    
    def modify_voiture(self, row, column):
        voiture = self.voitures[row]
        voiture.num_imma = self.voitures_table.item(row, 0).text() if self.voitures_table.item(row, 0) is not None else voiture.num_imma
        voiture.marque = self.voitures_table.item(row, 1).text() if self.voitures_table.item(row, 1) is not None else voiture.marque
        voiture.modele = self.voitures_table.item(row, 2).text() if self.voitures_table.item(row, 2) is not None else voiture.modele
        voiture.kilometrage = self.voitures_table.item(row, 3).text() if self.voitures_table.item(row, 3) is not None else voiture.kilometrage
        voiture.etat = self.voitures_table.item(row, 4).text() if self.voitures_table.item(row, 4) is not None else voiture.etat
        voiture.prix_location = self.voitures_table.item(row, 5).text() if self.voitures_table.item(row, 5) is not None else voiture.prix_location

        self.dbConnector.updateVoiture(voiture)
        
        print(self.voitures[0], voiture)        

    def delete_voiture(self):
        indices = self.voitures_table.selectionModel().selectedRows() 
        for index in sorted(indices):
            num_immat_voiture = self.voitures_table.item(index.row(), 0).text()
            self.voitures = [voiture for voiture in self.voitures if voiture.num_imma != num_immat_voiture]
            self.voitures_table.removeRow(index.row())
            self.dbConnector.deleteVoiture(num_immat_voiture)
        
        print(self.voitures)
        return


    def init_locataires(self, rows):
        for row in rows:
            self.locataires.append(
                Locataire(
                    row[0],
                    row[1],
                    row[2],
                    row[3]
                )
            )
            
            rowPosition = self.locataires_table.rowCount()
            self.locataires_table.insertRow(rowPosition)
            self.locataires_table.setItem(rowPosition , 0, QTableWidgetItem(self.locataires[-1].id_loc))
            self.locataires_table.setItem(rowPosition , 1, QTableWidgetItem(self.locataires[-1].nom))
            self.locataires_table.setItem(rowPosition , 2, QTableWidgetItem(self.locataires[-1].prenom))
            self.locataires_table.setItem(rowPosition , 3, QTableWidgetItem(self.locataires[-1].adresse))
    
    
    def add_locataire(self):
        self.locataires.append(
            Locataire(
                self.add_locataire_form_id_loc_input.text(),
                self.add_locataire_form_nom_input.text(),
                self.add_locataire_form_prenom_input.text(),
                self.add_locataire_form_adresse_input.text(),
            )
        )
        
        rowPosition = self.locataires_table.rowCount()
        self.locataires_table.insertRow(rowPosition)
        self.locataires_table.setItem(rowPosition , 0, QTableWidgetItem(self.locataires[-1].id_loc))
        self.locataires_table.setItem(rowPosition , 1, QTableWidgetItem(self.locataires[-1].nom))
        self.locataires_table.setItem(rowPosition , 2, QTableWidgetItem(self.locataires[-1].prenom))
        self.locataires_table.setItem(rowPosition , 3, QTableWidgetItem(self.locataires[-1].adresse))
        
        self.dbConnector.addLocataire(self.locataires[-1])
        return
        

    def modify_locataire(self, row, column):
        locataire = self.locataires[row]
        
        locataire.id_loc = self.locataires_table.item(row, 0).text() if self.locataires_table.item(row, 0) is not None else locataire.id_loc
        locataire.nom = self.locataires_table.item(row, 1).text() if self.locataires_table.item(row, 1) is not None else locataire.nom
        locataire.prenom = self.locataires_table.item(row, 2).text() if self.locataires_table.item(row, 2) is not None else locataire.prenom
        locataire.adresse = self.locataires_table.item(row, 3).text() if self.locataires_table.item(row, 3) is not None else locataire.adresse
        
        self.dbConnector.updateLocataire(locataire)
        
        print(self.locataires[0], locataire) 

    def delete_locataire(self):
        indices = self.locataires_table.selectionModel().selectedRows() 
        for index in sorted(indices):
            id_loc = self.locataires_table.item(index.row(), 0).text()
            self.locataires = [locataire for locataire in self.locataires if locataire.id_loc != id_loc]
            self.locataires_table.removeRow(index.row())
        
        # TODO : delete locataire in db
        self.dbConnector.deleteLocataire(id_loc)
        
        print(self.locataires)
        return

    def search_locataire(self):
        res = [index for (index, locataire) in enumerate(self.locataires) if locataire.id_loc == self.locataire_search_input.text()]
        if len(res) == 0:
            return
        
        index = self.locataires_table.model().index(res[0], 0)
        self.locataires_table.scrollTo(index)
        self.locataires_table.selectRow(index.row())

    def louer_voiture(self):
        pass

    def rendre_voiture(self):
        pass


def main():
    connector = DBConnector()
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    window = MainWindow(connector)
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()

if __name__ == '__main__':
    main()