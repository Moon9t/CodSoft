import argparse
from gui import launch_gui
from cli import launch_cli

def parse_arguments():
    parser = argparse.ArgumentParser(description="Modern Rock-Paper-Scissors Game")
    parser.add_argument('--mode', choices=['cli', 'gui'], default='gui', help="Select interface mode")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.mode == 'gui':
        launch_gui()
    else:
        launch_cli()

if __name__ == "__main__":
    main()