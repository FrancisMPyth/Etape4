# Fichier controllers.py

import os
import json
from tkinter import Tk, Label, Entry, Button, messagebox, Toplevel, Text, END, Checkbutton, IntVar
from models import Player, Tournament


class MenuController:
    def __init__(self):
        self.player_db = []  # Base de données des joueurs
        self.tournament_db = []  # Base de données des tournois
        self.data_dir = "data"  # Nom du répertoire de données

        # Créer le répertoire "data" s'il n'existe pas
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Créer le répertoire "joueurs" s'il n'existe pas
        players_dir = os.path.join(self.data_dir, "joueurs")
        if not os.path.exists(players_dir):
            os.makedirs(players_dir)

        # Créer le répertoire "tournois" s'il n'existe pas
        tournaments_dir = os.path.join(self.data_dir, "tournois")
        if not os.path.exists(tournaments_dir):
            os.makedirs(tournaments_dir)

        self.root = Tk()
        self.root.title("Gestion de Tournoi")

        self.add_player_button = Button(self.root, text="Ajouter un joueur", command=self.add_player)
        self.add_player_button.pack()

        self.display_players_button = Button(self.root, text="Afficher les joueurs", command=self.display_players)
        self.display_players_button.pack()

        self.create_tournament_button = Button(self.root, text="Créer un tournoi", command=self.create_tournament)
        self.create_tournament_button.pack()

        self.display_tournaments_button = Button(self.root, text="Liste des tournois", command=self.display_tournaments)
        self.display_tournaments_button.pack()

    def run(self):
        self.load_players_from_json()
        self.load_tournaments_from_json()
        self.root.mainloop()

    def add_player(self):
        self.root.destroy()  # Ferme la fenêtre principale

        add_player_window = Toplevel()
        add_player_window.title("Ajouter un joueur")

        last_name_label = Label(add_player_window, text="Nom de famille:")
        last_name_label.pack()
        last_name_entry = Entry(add_player_window)
        last_name_entry.pack()

        first_name_label = Label(add_player_window, text="Prénom:")
        first_name_label.pack()
        first_name_entry = Entry(add_player_window)
        first_name_entry.pack()

        chess_id_label = Label(add_player_window, text="Identifiant national d'échecs:")
        chess_id_label.pack()
        chess_id_entry = Entry(add_player_window)
        chess_id_entry.pack()

        def save_player():
            last_name = last_name_entry.get()
            first_name = first_name_entry.get()
            chess_id = chess_id_entry.get()

            if last_name and first_name and chess_id:
                player = Player(last_name, first_name, chess_id)
                self.player_db.append(player)
                self.save_players_to_json()

                messagebox.showinfo("Succès", "Le joueur a été ajouté avec succès.")
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

            add_player_window.destroy()  # Ferme la fenêtre d'ajout de joueur
            self.root.deiconify()  # Réaffiche la fenêtre principale

        save_button = Button(add_player_window, text="Enregistrer", command=save_player)
        save_button.pack()

        add_player_window.mainloop()

    def display_players(self):
        self.load_players_from_json()  # Charger les joueurs à partir du fichier JSON
        self.root.withdraw()  # Cacher la fenêtre principale

        display_players_window = Toplevel()
        display_players_window.title("Liste des joueurs")

        players_label = Label(display_players_window, text="Liste des joueurs :")
        players_label.pack()

        players_text = Text(display_players_window)
        players_text.pack()

        players_sorted = sorted(self.player_db, key=lambda player: player.last_name)

        for player in players_sorted:
            players_text.insert(END, f"{player.last_name}, {player.first_name} ({player.chess_id})\n")

        ok_button = Button(display_players_window, text="OK", command=lambda: self.return_to_menu(display_players_window))
        ok_button.pack()

        display_players_window.protocol("WM_DELETE_WINDOW", lambda: self.return_to_menu(display_players_window))

        display_players_window.mainloop()

    def create_tournament(self):
        self.root.destroy()  # Ferme la fenêtre principale

        create_tournament_window = Toplevel()
        create_tournament_window.title("Créer un tournoi")

        name_label = Label(create_tournament_window, text="Nom du tournoi:")
        name_label.pack()
        name_entry = Entry(create_tournament_window)
        name_entry.pack()

        location_label = Label(create_tournament_window, text="Lieu du tournoi:")
        location_label.pack()
        location_entry = Entry(create_tournament_window)
        location_entry.pack()

        start_date_label = Label(create_tournament_window, text="Date de début (YYYY-MM-DD):")
        start_date_label.pack()
        start_date_entry = Entry(create_tournament_window)
        start_date_entry.pack()

        end_date_label = Label(create_tournament_window, text="Date de fin (YYYY-MM-DD):")
        end_date_label.pack()
        end_date_entry = Entry(create_tournament_window)
        end_date_entry.pack()

        num_players_label = Label(create_tournament_window, text="Nombre de participants:")
        num_players_label.pack()
        num_players_entry = Entry(create_tournament_window)
        num_players_entry.pack()

        def save_tournament():
            name = name_entry.get()
            location = location_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            num_players = num_players_entry.get()

            if name and location and start_date and end_date and num_players:
                tournament = Tournament(name, location, start_date, end_date, num_players)
                self.tournament_db.append(tournament)
                self.save_tournament_to_json(tournament)

                messagebox.showinfo("Succès", "Le tournoi a été créé avec succès.")
                self.manage_tournament(tournament)  # Appeler la fonction de gestion du tournoi
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

            create_tournament_window.destroy()  # Ferme la fenêtre de création de tournoi
            self.root.deiconify()  # Réaffiche la fenêtre principale

        save_button = Button(create_tournament_window, text="Enregistrer", command=save_tournament)
        save_button.pack()

        create_tournament_window.mainloop()

    def display_tournaments(self):
        self.load_tournaments_from_json()  # Charger les tournois à partir du fichier JSON
        self.root.withdraw()  # Cacher la fenêtre principale

        display_tournaments_window = Toplevel()
        display_tournaments_window.title("Liste des tournois")

        tournaments_label = Label(display_tournaments_window, text="Liste des tournois :")
        tournaments_label.pack()

        tournaments_text = Text(display_tournaments_window)
        tournaments_text.pack()

        for tournament in self.tournament_db:
            tournaments_text.insert(END, f"Nom : {tournament.name}\n")
            tournaments_text.insert(END, f"Lieu : {tournament.location}\n")
            tournaments_text.insert(END, f"Date de début : {tournament.start_date}\n")
            tournaments_text.insert(END, f"Date de fin : {tournament.end_date}\n")
            tournaments_text.insert(END, f"Nombre de joueurs : {len(tournament.players)}\n")
            tournaments_text.insert(END, "\n")

        manage_button = Button(display_tournaments_window, text="Gérer le tournoi", command=lambda: self.manage_tournament(display_tournaments_window, tournament))
        manage_button.pack()

        ok_button = Button(display_tournaments_window, text="OK", command=lambda: self.return_to_menu(display_tournaments_window))
        ok_button.pack()

        display_tournaments_window.protocol("WM_DELETE_WINDOW", lambda: self.return_to_menu(display_tournaments_window))

        display_tournaments_window.mainloop()

    def return_to_menu(self, window):
        window.destroy()
        self.root.deiconify()

    def manage_tournament(self, window, tournament):
        selected_players = []  # Liste des joueurs sélectionnés

        manage_tournament_window = Toplevel()
        manage_tournament_window.title("Gestion du tournoi")

        # Afficher la liste des joueurs disponibles avec des cases à cocher pour les sélectionner
        players_label = Label(manage_tournament_window, text="Liste des joueurs disponibles :")
        players_label.pack()

        for player in self.player_db:
            var = IntVar()
            checkbox = Checkbutton(manage_tournament_window, text=f"{player.last_name}, {player.first_name} ({player.chess_id})", variable=var)
            checkbox.pack()
            selected_players.append((player, var))

        def save_selected_players():
            # Enregistrer les joueurs sélectionnés dans le rapport JSON
            selected_players_data = []
            for player, var in selected_players:
                if var.get() == 1:
                    selected_players_data.append(player.__dict__)

            tournament_dir = os.path.join(self.data_dir, "tournois", tournament.name)
            if not os.path.exists(tournament_dir):
                os.makedirs(tournament_dir)

            file_path = os.path.join(tournament_dir, "selected_players.json")
            with open(file_path, "w") as file:
                json.dump(selected_players_data, file)

            messagebox.showinfo("Succès", "La liste des joueurs sélectionnés a été enregistrée.")

        save_button = Button(manage_tournament_window, text="Enregistrer la sélection", command=save_selected_players)
        save_button.pack()

        window.destroy()
        self.root.withdraw()
        manage_tournament_window.mainloop()

    def save_tournament_to_json(self, tournament):
        tournaments_dir = os.path.join(self.data_dir, "tournois")
        if not os.path.exists(tournaments_dir):
            os.makedirs(tournaments_dir)

        file_path = os.path.join(tournaments_dir, f"{tournament.name}.json")
        with open(file_path, "w") as file:
            tournament_data = tournament.__dict__
            json.dump(tournament_data, file)

    def save_players_to_json(self):
        file_path = os.path.join(self.data_dir, "joueurs", "players.json")
        with open(file_path, "w") as file:
            players_data = [player.__dict__ for player in self.player_db]
            json.dump(players_data, file)

    def load_players_from_json(self):
        file_path = os.path.join(self.data_dir, "joueurs", "players.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                players_data = json.load(file)
                self.player_db = [Player(player["last_name"], player["first_name"], player["birth_date"], player["chess_id"]) for player in players_data]

    def load_tournaments_from_json(self):
        tournaments_dir = os.path.join(self.data_dir, "tournois")
        if os.path.exists(tournaments_dir):
            for filename in os.listdir(tournaments_dir):
                file_path = os.path.join(tournaments_dir, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        tournament_data = json.load(file)
                        tournament = Tournament(**tournament_data)
                        self.tournament_db.append(tournament)

menu_controller = MenuController()
menu_controller.run()


       

