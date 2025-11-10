class Player:
    def __init__(self, data):
        self.name = data["name"]
        teams = data.get("team", "")
        self.team = ", ".join(teams) if isinstance(teams, list) else teams
        self.games = data.get("games", 0)
        self.goals = data.get("goals", 0)
        self.assists = data.get("assists", 0)
        self.points = self.goals + self.assists
        self.nationality = (data.get("nationality") or "").upper()

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals} + {self.assists} = {self.points}"
