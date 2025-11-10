import requests
from player import Player

class PlayerReader:
    BASE = "https://studies.cs.helsinki.fi/nhlstats/{season}/players"

    def get_players(self, season: str):
        url = self.BASE.format(season=season)
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return [Player(p) for p in r.json()]
