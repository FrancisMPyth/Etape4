# gui.py

import tkinter as tk
from tkinter import messagebox
from models import Tournament


class TournamentGUI:
    def __init__(self):
        self.tournament = None
        self.round = 1  # Round en cours

        self.window = tk.Tk()
        self.window.title("Tournoi")
        
        self.round_label = tk.Label(self.window, text=f"Round {self.round}")
        self.round_label.pack()

        self.matches_frame = tk.Frame(self.window)
        self.matches_frame.pack()

        self.matches_labels = []
        self.winner_vars = []

        self.submit_button = tk.Button(self.window, text="Valider", command=self.submit_results)
        self.submit_button.pack()

    def create_tournament(self):
        # Ajoutez ici la logique de création du tournoi
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")
        start_date = input("Date de début (YYYY-MM-DD) : ")
        end_date = input("Date de fin (YYYY-MM-DD) : ")
        num_rounds = int(input("Nombre de tours : "))

        # Créez l'objet Tournament avec les informations saisies
        self.tournament = Tournament(name, location, start_date, end_date, num_rounds)

        # Mettez à jour l'interface graphique pour afficher les paires de la première ronde
        self.update_round()

    def submit_results(self):
        # Ajoutez ici la logique de soumission des résultats

        results = []
        for i, var in enumerate(self.winner_vars):
            if var.get():
                match = self.tournament.rounds[self.round-1]["matches"][i]
                results.append((match[0], match[1]))

        # Mettez à jour les scores en fonction des résultats
        self.tournament.update_scores(results)

        # Passez au prochain round ou terminez le tournoi
        if self.round < self.tournament.num_rounds:
            self.round += 1
            self.update_round()
        else:
            messagebox.showinfo("Tournoi terminé", "Le tournoi est terminé.")
            self.window.destroy()

    def update_round(self):
        # Ajoutez ici la logique de mise à jour de l'interface graphique pour afficher les paires du round en cours

        self.round_label.config(text=f"Round {self.round}")
        for label in self.matches_labels:
            label.pack_forget()
        for var in self.winner_vars:
            var.set(False)
        self.matches_labels.clear()
        self.winner_vars.clear()

        for match in self.tournament.rounds[self.round-1]["matches"]:
            match_label = tk.Label(self.matches_frame, text=f"{match[0].last_name} vs {match[1].last_name}")
            match_label.pack()
            self.matches_labels.append(match_label)

            winner_var = tk.BooleanVar()
            winner_checkbox = tk.Checkbutton(self.matches_frame, text="Gagnant", variable=winner_var)
            winner_checkbox.pack()
            self.winner_vars.append(winner_var)

    def run(self):
        # Ajoutez ici la logique pour démarrer l'interface graphique et créer le tournoi
        self.create_tournament()
        self.window.mainloop()
