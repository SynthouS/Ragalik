import inquirer
from hellping import show_help
from game import Game
import os
import importlib.util
import sys

def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    welcome()
    questions = [
        inquirer.List('action',
                      message="What would you like to do?",
                      choices=['Start game', 'Help', 'Mods', 'Exit'],
                    ),
    ]

    answers = inquirer.prompt(questions)

    if answers['action'] == 'Start game':
        game = Game()
        game.play()
    elif answers['action'] == 'Help':
        show_help()
        show_menu()
    elif answers['action'] == 'Mods':
        load_mod()
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
                __/ |     © 2024       
               |___/    
    © Synthous, all knights reserved     
    """
    print(art)

def load_mod():
    mod_path = input("Enter relative path (e.g mods/ExMod): ").strip()
    main_file_path = os.path.join(os.getcwd(), mod_path, 'main.py')

    try:
        if os.path.exists(main_file_path):
            spec = importlib.util.spec_from_file_location("mod_main", main_file_path)
            mod_main = importlib.util.module_from_spec(spec)
            sys.modules["mod_main"] = mod_main
            spec.loader.exec_module(mod_main)
            print(f"Loading mod: {mod_path}")

            if hasattr(mod_main, 'main'):
                return_value = mod_main.main()
                if return_value is not None and return_value == "exit":
                    print("Exit from mod...")
                    return
            else:
                print(f"Function main() dont find '{mod_path}'.")
                input("Press enter...")
        else:
            print(f"Mod '{mod_path}' dont find. Check, is there a 'main.py' file in the mod folder.")
            input("Press enter...")
    except Exception as e:
        print(f"Error while loading mod: {e}")
        input("Press enter...")
    
    show_menu()

def main():
    welcome()
    show_menu()

if __name__ == "__main__":
    main()