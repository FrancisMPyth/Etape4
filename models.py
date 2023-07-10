# Fichier models.py

from __future__ import annotations

import json
from typing import List, Dict


class Player:
    player_counter = 0

    def __init__(self, last_name, first_name, birth_date, chess_id, tournament_id=None):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.tournament_id = tournament_id

    @classmethod
    def generate_chess_id(cls):
        cls.player_counter += 1
        return f"Jr{cls.player_counter:02d}"


class Tournament:
    def __init__(self, name, location, start_date, end_date, num_rounds=4, players=None, rounds=None, current_round=None):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.num_rounds = num_rounds
        self.players = players or []
        self.rounds = rounds or []
        self.current_round = current_round

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            json.dump(self.__dict__, file)

    @staticmethod
    def load_from_file(filename):
        from models import Tournament  # Importation retardée ici pour éviter la circularité
        with open(filename, "r") as file:
            data = json.load(file)
            tournament = Tournament("", "", "", "")
            tournament.__dict__.update(data)
            return tournament
