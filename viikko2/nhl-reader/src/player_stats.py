class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, season: str, nationality: str):
        nat = (nationality or "").upper()
        players = [p for p in self.reader.get_players(season) if p.nationality == nat]
        return sorted(players, key=lambda p: p.points, reverse=True)
