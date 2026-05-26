# rps_game.py
import random
import sqlite3
from datetime import datetime
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

class RPSTracker:
    def __init__(self):
        self.conn = sqlite3.connect('game_stats.db')
        self.create_tables()
        self.player_pattern = defaultdict(lambda: defaultdict(int))
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                date TEXT,
                player_choice TEXT,
                ai_choice TEXT,
                result TEXT,
                game_mode TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                date TEXT,
                games_played INTEGER,
                player_wins INTEGER,
                ai_wins INTEGER,
                ties INTEGER
            )
        ''')
        self.conn.commit()
    
    def record_game(self, player, ai, result, mode):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO games (date, player_choice, ai_choice, result, game_mode)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), player, ai, result, mode))
        self.conn.commit()
        
        # Update pattern for AI learning
        self.player_pattern[player]['count'] += 1
    
    def get_statistics(self):
        cursor = self.conn.cursor()
        
        # Overall stats
        cursor.execute("SELECT COUNT(*), SUM(CASE WHEN result='win' THEN 1 ELSE 0 END), "
                      "SUM(CASE WHEN result='loss' THEN 1 ELSE 0 END), "
                      "SUM(CASE WHEN result='tie' THEN 1 ELSE 0 END) FROM games")
        total, wins, losses, ties = cursor.fetchone()
        
        # Win rate per choice
        cursor.execute("SELECT player_choice, COUNT(*), SUM(CASE WHEN result='win' THEN 1 ELSE 0 END) "
                      "FROM games GROUP BY player_choice")
        choice_stats = cursor.fetchall()
        
        return total, wins or 0, losses or 0, ties or 0, choice_stats

class AdaptiveAI:
    def __init__(self, tracker):
        self.tracker = tracker
    
    def predict_player_move(self):
        # Simple adaptive AI based on player's most common move
        if not self.tracker.player_pattern:
            return random.choice(['rock', 'paper', 'scissors'])
        
        most_common = max(self.tracker.player_pattern.items(), 
                         key=lambda x: x[1]['count'])[0]
        
        # Counter the most common move
        counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
        return counters[most_common]
    
    def get_move(self, difficulty='medium'):
        if difficulty == 'easy':
            return random.choice(['rock', 'paper', 'scissors'])
        elif difficulty == 'hard':
            return self.predict_player_move()
        else:  # medium - 70% adaptive, 30% random
            if random.random() < 0.7:
                return self.predict_player_move()
            else:
                return random.choice(['rock', 'paper', 'scissors'])

class RPSGame:
    def __init__(self):
        self.tracker = RPSTracker()
        self.ai = AdaptiveAI(self.tracker)
        self.choices = ['rock', 'paper', 'scissors']
        self.rules = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }
    
    def determine_winner(self, player, ai):
        if player == ai:
            return 'tie'
        elif self.rules[player] == ai:
            return 'win'
        else:
            return 'loss'
    
    def play_match(self, mode='best_of_3', difficulty='medium'):
        player_score = 0
        ai_score = 0
        rounds_needed = 0
        
        if mode == 'best_of_3':
            rounds_needed = 2
        elif mode == 'best_of_5':
            rounds_needed = 3
        elif mode == 'best_of_10':
            rounds_needed = 6
        
        round_num = 1
        
        while player_score < rounds_needed and ai_score < rounds_needed:
            console.print(Panel(f"[bold cyan]Round {round_num}[/bold cyan]"))
            console.print(f"Score: You {player_score} - {ai_score} AI")
            
            player_choice = Prompt.ask("Your choice", choices=['rock', 'paper', 'scissors'])
            ai_choice = self.ai.get_move(difficulty)
            
            console.print(f"AI chose: [bold magenta]{ai_choice}[/bold magenta]")
            
            result = self.determine_winner(player_choice, ai_choice)
            
            if result == 'win':
                console.print("[green]✓ You win this round![/green]")
                player_score += 1
            elif result == 'loss':
                console.print("[red]✗ AI wins this round![/red]")
                ai_score += 1
            else:
                console.print("[yellow]= Tie![/yellow]")
            
            self.tracker.record_game(player_choice, ai_choice, result, mode)
            round_num += 1
        
        console.print(Panel(f"[bold]FINAL RESULT: You {player_score} - {ai_score} AI[/bold]"))
        
        if player_score > ai_score:
            console.print("[green]🏆 You won the match! 🏆[/green]")
        else:
            console.print("[red]AI won the match! Better luck next time![/red]")
    
    def show_dashboard(self):
        total, wins, losses, ties, choice_stats = self.tracker.get_statistics()
        
        console.print(Panel.fit("[bold blue]Game Statistics Dashboard[/bold blue]", border_style="blue"))
        
        if total == 0:
            console.print("[yellow]No games played yet[/yellow]")
            return
        
        win_rate = (wins / total) * 100 if total > 0 else 0
        
        stats_table = Table(title="Overall Stats")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        stats_table.add_row("Total Games", str(total))
        stats_table.add_row("Wins", str(wins))
        stats_table.add_row("Losses", str(losses))
        stats_table.add_row("Ties", str(ties))
        stats_table.add_row("Win Rate", f"{win_rate:.1f}%")
        console.print(stats_table)
        
        if choice_stats:
            choice_table = Table(title="Performance by Choice")
            choice_table.add_column("Choice", style="cyan")
            choice_table.add_column("Games", style="green")
            choice_table.add_column("Wins", style="yellow")
            choice_table.add_column("Win %", style="magenta")
            
            for choice, games, choice_wins in choice_stats:
                win_pct = (choice_wins / games) * 100 if games > 0 else 0
                choice_table.add_row(choice, str(games), str(choice_wins), f"{win_pct:.1f}%")
            
            console.print(choice_table)

def main():
    game = RPSGame()
    console.print(Panel.fit("[bold yellow]🔥 Advanced Rock-Paper-Scissors with AI 🔥[/bold yellow]", border_style="yellow"))
    
    while True:
        console.print("\n[1] Play Match")
        console.print("[2] View Statistics")
        console.print("[3] Exit")
        
        choice = Prompt.ask("Choose option", choices=["1","2","3"])
        
        if choice == "1":
            mode = Prompt.ask("Game mode", choices=["best_of_3", "best_of_5", "best_of_10"])
            difficulty = Prompt.ask("AI Difficulty", choices=["easy", "medium", "hard"])
            game.play_match(mode, difficulty)
        
        elif choice == "2":
            game.show_dashboard()
        
        elif choice == "3":
            console.print("[bold blue]Thanks for playing! 🎮[/bold blue]")
            break

if __name__ == "__main__":
    main()