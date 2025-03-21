import random
from enum import Enum
import time

class GameMode(Enum):
    CLASSIC = "Classic"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class GameLogic:
    def __init__(self):
        self.classic_choices = ['rock', 'paper', 'scissors']
        self.advanced_choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
        self.current_mode = GameMode.CLASSIC
        self.combo_count = 0
        self.last_win_time = time.time()
        
        # Advanced rules including lizard and spock
        self.advanced_rules = {
            'rock': {'scissors': 'win', 'lizard': 'win', 'paper': 'lose', 'spock': 'lose', 'rock': 'tie'},
            'paper': {'rock': 'win', 'spock': 'win', 'scissors': 'lose', 'lizard': 'lose', 'paper': 'tie'},
            'scissors': {'paper': 'win', 'lizard': 'win', 'rock': 'lose', 'spock': 'lose', 'scissors': 'tie'},
            'lizard': {'paper': 'win', 'spock': 'win', 'rock': 'lose', 'scissors': 'lose', 'lizard': 'tie'},
            'spock': {'rock': 'win', 'scissors': 'win', 'paper': 'lose', 'lizard': 'lose', 'spock': 'tie'}
        }
        
        # Classic rules
        self.classic_rules = {
            'rock': {'scissors': 'win', 'paper': 'lose', 'rock': 'tie'},
            'paper': {'rock': 'win', 'scissors': 'lose', 'paper': 'tie'},
            'scissors': {'paper': 'win', 'rock': 'lose', 'scissors': 'tie'}
        }
        
        # AI patterns for expert mode
        self.player_history = []
        self.pattern_length = 3

    def set_mode(self, mode: GameMode):
        self.current_mode = mode
        self.combo_count = 0
        self.player_history = []

    def analyze_pattern(self):
        if len(self.player_history) < self.pattern_length:
            return random.choice(self.get_current_choices())
            
        # Look for patterns in player's moves
        last_sequence = self.player_history[-self.pattern_length:]
        for i in range(len(self.player_history) - self.pattern_length):
            if self.player_history[i:i+self.pattern_length] == last_sequence:
                next_move = self.player_history[i+self.pattern_length]
                # Choose winning move against predicted next move
                return self.get_winning_move(next_move)
                
        return random.choice(self.get_current_choices())

    def get_winning_move(self, player_move):
        rules = self.advanced_rules if self.current_mode != GameMode.CLASSIC else self.classic_rules
        winning_moves = [move for move, outcomes in rules.items() if outcomes.get(player_move) == 'win']
        return random.choice(winning_moves)

    def get_current_choices(self):
        return self.advanced_choices if self.current_mode != GameMode.CLASSIC else self.classic_choices

    def play_round(self, player_choice):
        self.player_history.append(player_choice)
        
        # Choose computer move based on mode
        if self.current_mode == GameMode.EXPERT:
            computer_choice = self.analyze_pattern()
        else:
            computer_choice = random.choice(self.get_current_choices())
        
        # Get appropriate ruleset
        rules = self.advanced_rules if self.current_mode != GameMode.CLASSIC else self.classic_rules
        outcome = rules[player_choice][computer_choice]
        
        # Update combo system
        current_time = time.time()
        if outcome == 'win':
            if current_time - self.last_win_time < 2.0:  # 2 second window for combos
                self.combo_count += 1
            else:
                self.combo_count = 1
            self.last_win_time = current_time
        else:
            self.combo_count = 0
            
        return {
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'outcome': outcome,
            'combo': self.combo_count
        }

    def get_move_description(self, move1, move2):
        descriptions = {
            ('rock', 'scissors'): 'Rock crushes Scissors',
            ('rock', 'lizard'): 'Rock crushes Lizard',
            ('paper', 'rock'): 'Paper covers Rock',
            ('paper', 'spock'): 'Paper disproves Spock',
            ('scissors', 'paper'): 'Scissors cuts Paper',
            ('scissors', 'lizard'): 'Scissors decapitates Lizard',
            ('lizard', 'paper'): 'Lizard eats Paper',
            ('lizard', 'spock'): 'Lizard poisons Spock',
            ('spock', 'rock'): 'Spock vaporizes Rock',
            ('spock', 'scissors'): 'Spock smashes Scissors'
        }
        return descriptions.get((move1, move2), "")
