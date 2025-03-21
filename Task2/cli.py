from game_logic import GameLogic

def launch_cli():
    game = GameLogic()
    scores = {'player': 0, 'computer': 0}
    
    print("Welcome to Rock-Paper-Scissors!")
    
    while True:
        print("\nCurrent Score:")
        print(f"Player: {scores['player']} | Computer: {scores['computer']}")
        print("\nChoose: rock, paper, scissors (or 'q' to quit)")
        
        choice = input("> ").lower().strip()
        if choice == 'q':
            break
            
        if choice not in game.choices:
            print("Invalid choice! Please try again.")
            continue
            
        result = game.play_round(choice)
        print(f"\nYou chose: {choice}")
        print(f"Computer chose: {result['computer_choice']}")
        
        if result['outcome'] == 'win':
            print("You win! 🎉")
            scores['player'] += 1
        elif result['outcome'] == 'lose':
            print("You lose! 😢")
            scores['computer'] += 1
        else:
            print("It's a tie! 🤝")
            
    print("\nFinal Score:")
    print(f"Player: {scores['player']} | Computer: {scores['computer']}")
    print("Thanks for playing!")