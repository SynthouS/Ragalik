import inquirer
import os

import random
from maps import rooms, boss_fight

class Game:
    def __init__(self):
        self.current_room = 0
        self.player_pos = [1, 1]
        self.room = rooms[self.current_room]
        self.remaining_moves = 35
        self.cooldown = 0  # Cooldown for interacting with '$'
        self.e_pos = [0, 0]  # Position of E
        self.spawn_e()  # Spawn E at a random position
        self.moves_made = 0  # Counter for moves made
        self.bombs = 3  # Initial number of bombs

    def spawn_e(self):
        while True:
            y = random.randint(0, len(self.room) - 1)
            x = random.randint(0, len(self.room[y]) - 1)
            if self.room[y][x] != '#' and [y, x] != self.player_pos:
                self.e_pos = [y, x]
                break

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(len(self.room)):
            row = list(self.room[y])
            if (self.player_pos[0], self.player_pos[1]) == (y, self.player_pos[1]):
                row[self.player_pos[1]] = '@'
            if self.moves_made >= 10 and self.e_pos[0] == y and 0 <= self.e_pos[1] < len(row):
                row[self.e_pos[1]] = 'E'  # Draw E only after 10 moves
            print(''.join(row))
        
        print(f"Remaining moves: {self.remaining_moves}")
        print(f"Bombs left: {self.bombs}")  # Display number of bombs
        print(f"Bonus cooldown remaining: {self.cooldown}")

    def move(self, direction):
        if self.remaining_moves <= 0:
            self.game_over()

        y, x = self.player_pos
        if direction == 'w' and self.room[y - 1][x] != '#':
            self.player_pos[0] -= 1
        elif direction == 's' and self.room[y + 1][x] != '#':
            self.player_pos[0] += 1
        elif direction == 'a' and self.room[y][x - 1] != '#':
            self.player_pos[1] -= 1
        elif direction == 'd' and self.room[y][x + 1] != '#':
            self.player_pos[1] += 1
        elif direction == 'bomb':
            self.use_bomb()  # Use bomb if command is 'bomb'
            return
        
        self.moves_made += 1
        self.move_e_towards_player()

        if self.moves_made >= 10 and self.player_pos == self.e_pos:
            self.remaining_moves -= 15
            print("You touched Enemy! You lost 15 moves.")
            input("Press Enter to continue...")
            self.spawn_e()

        if self.room[self.player_pos[0]][self.player_pos[1]] == 'S':
            loss = random.randint(5, 20)
            self.remaining_moves -= loss
            print(f"You touched Spikes! You lost {loss} moves.")
            input("Press Enter to continue...")

        if self.room[self.player_pos[0]][self.player_pos[1]] == 'W':
            self.win()

        if self.room[self.player_pos[0]][self.player_pos[1]] == 'O':
            self.current_room = random.choice(range(len(rooms)))
            self.room = rooms[self.current_room]
            self.player_pos = [1, 1]
            self.spawn_e()
            self.remaining_moves += 5

        if self.room[self.player_pos[0]][self.player_pos[1]] == '$' and self.cooldown == 0:
            self.trigger_random_event()

        if self.remaining_moves >= 100:
            self.current_room = random.choice(range(len(boss_fight)))
            self.room = boss_fight[self .current_room]
            self.player_pos = [1, 1]
            self.spawn_e()

        self.remaining_moves -= 1
        self.cooldown = max(0, self.cooldown - 1)

        if self.remaining_moves <= 0:
            self.game_over()

    def use_bomb(self):
        if self.bombs > 0:
            self.bombs -= 1
            if abs(self.e_pos[0] - self.player_pos[0]) <= 2 and abs(self.e_pos[1] - self.player_pos[1]) <= 2:
                self.e_pos = [0, 0]  # Remove enemy
                print("Bomb exploded and removed the enemy!")
                input("Press Enter to continue...")
            else:
                print("Bomb exploded, but there was no enemy nearby.")
                input("Press Enter to continue...")
        else:
            print("You don't have any bombs left!")
            input("Press Enter to continue...")

    def move_e_towards_player(self):
        if self.e_pos[0] < self.player_pos[0]:
            self.e_pos[0] += 1
        elif self.e_pos[0] > self.player_pos[0]:
            self.e_pos[0] -= 1

        if self.e_pos[1] < self.player_pos[1]:
            self.e_pos[1] += 1
        elif self.e_pos[1] > self.player_pos[1]:
            self.e_pos[1] -= 1

    def trigger_random_event(self):
        events = [
            (20, "You gained 20 moves!"),
            (-5, "You lost 5 moves."),
            (-5, "You lost 5 moves."),
            (5, "You gained 5 moves!"),
            (0, "You have been teleported to another room!"),
            (1, "You found a bomb!")  # New event for gaining a bomb
        ]

        event = random.choice(events)

        if event[0] > 0:
            if event[0] == 1:  # Check if the event is for gaining a bomb
                self.bombs += 1
                print(event[1])
            else:
                self.remaining_moves += event[0]
                print(event[1])
        else:
            self.current_room = random.choice([i for i in range(len(rooms)) if i != self.current_room])
            self.room = rooms[self.current_room]
            self.player_pos = [1, 1]
            print(event[1])

        self.cooldown = 15
        input("Press Enter to continue...")

    def game_over(self):
        art = fr"""
                                                        
          __ _  __ _ _ __ ___   ___    _____   _____ _ __ 
         / _` |/ _` | '_ ` _ \ / _ \  / _ \ \ / / _ \ '__|
        | (_| | (_| | | | | | |  __/ | (_) \ V /  __/ |   
         \__, |\__,_|_| |_| |_|\___|  \___/ \_/ \___|_|   
          __/ |                                         
          |___/                                          
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(art)
        print("No moves left.")
        print("Try again")
        exit()

    def win(self):
        art2 = fr"""
                                              _       
                                             (_)      
                 _   _  ___  _   _  __      ___ _ __  
                | | | |/ _ \| | | | \ \ /\ / / | '_ \ 
                | |_| | (_) | |_| |  \ V  V /| | | | |
                 \__, |\___/ \__,_|   \_/\_/ |_|_| |_|
                  __/ |            EXMODEEEEEE!       
                 |___/                          
            """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(art2)
        print("game by Ragmods Team")
        print("made by Python")
        print("And.... Thank you for play us Mod! -, Ragmods Team")
        exit()

    def play(self):
        while True:
            self.draw()
            move = input("Enter action: ").strip().lower()
            if move in ['q', 'exit']:
                print("Quitting...")
                break
            else:
                self.move(move)

def show_help():
    print("ExMode dont's have Help, help yourself.")
    input("press Enter...")

def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    welcome()
    questions = [
        inquirer.List('action',
                      message="What would you like to do?",
                      choices=['Start game', 'Help', 'Exit'],
                    ),
    ]

    answers = inquirer.prompt(questions)

    if answers['action'] == 'Start game':
        game = Game()
        game.play()
    elif answers['action'] == 'Help':
        show_help()
        show_menu()
    else:
        print("Quitting...")

def welcome():
    art = fr"""
    Welcome to
                           _ _ _     
                          | (_) |    
     _ __ __ _  __ _  __ _| |_| | __ 
    | '__/ _` |/ _` |/ _` | | | |/ / 
    | | | (_| | (_| | (_| | | |   <  
    |_|  \__,_|\__, |\__,_|_|_|_|\_\ 
                __/ | EXmod!1! © 2024       
               |___/    
    © Ragmods Team, all knights reserved

    P.S Subscribe own telegram channel! 
    https://t.me/RagalikMods     
    """
    print(art)

def main():
    welcome()
    show_menu()

if __name__ == "__main__":
    main()