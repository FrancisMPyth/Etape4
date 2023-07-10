# Fichier views.py

class PlayerView:
    def display_players(self, players):
        print("Liste des joueurs :")
        for player in players:
            print(f"{player.last_name}, {player.first_name} ({player.chess_id})")


    def display_player_details(self, player):
        print("Détails du joueur :")
        print(f"Nom : {player.last_name}")
        print(f"Prénom : {player.first_name}")
        print(f"Date de naissance : {player.birth_date}")
        print(f"Identifiant national d'échecs : {player.chess_id}")


class TournamentView:
    def display_tournaments(self, tournaments):
        print("Liste des tournois :")
        for tournament in tournaments:
            print(f"{tournament.name} ({tournament.location})")

    def display_tournament_details(self, tournament):
        print("Détails du tournoi :")
        print(f"Nom : {tournament.name}")
        print(f"Lieu : {tournament.location}")
        print(f"Date de début : {tournament.start_date}")
        print(f"Date de fin : {tournament.end_date}")

    def display_tournament_rounds_and_matches(self, tournament):
        print("Rounds et matchs du tournoi :")
        for i, round in enumerate(tournament.rounds):
            print(f"Round {i + 1}:")
            for match in round["matches"]:
                player1 = match[0]
                player2 = match[1]
                print(f"{player1.last_name}, {player1.first_name} vs {player2.last_name}, {player2.first_name}")
