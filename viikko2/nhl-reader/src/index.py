from rich.console import Console
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats

def main():
    console = Console()

    season = console.input("Anna kausi (esim. [bold]2024-25[/bold]): ").strip()
    country = console.input("Anna maa (esim. [bold]FIN[/bold]): ").strip().upper()

    reader = PlayerReader()
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(season, country)

    console.print(f"\n[bold]Season {season} players from {country}[/bold]\n")

    table = Table(show_header=True, header_style="bold magenta")

    # Väritetyt sarakkeet
    table.add_column("Player", style="bold cyan")
    table.add_column("Teams", style="yellow")
    table.add_column("G", justify="right", style="bold green")
    table.add_column("A", justify="right", style="bold green")
    table.add_column("P", justify="right", style="bold green")

    for p in players:
        table.add_row(
            p.name,
            p.team,
            str(p.goals),
            str(p.assists),
            str(p.points),
        )

    console.print(table)

if __name__ == "__main__":
    main()
