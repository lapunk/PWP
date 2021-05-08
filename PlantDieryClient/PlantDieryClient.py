import sys
from plants_cli import Plant
from diary_cli import Diary
from specie_plants_cli import Specie

def main():
    '''Main menu'''
    while True:
        print_welcome()
        giv_input = input("choice: ")
        if giv_input == "1":
            plants_menu()
        elif giv_input == "2":
            plantsgen_menu()
        elif giv_input == "3":
            diary_menu()
        elif giv_input == "4":
            sys.exit(0)
        else:
            print("Invalid option: {}".format(giv_input))

def plants_menu():
    ''' Controls plants related actions'''
    plant = Plant()
    while True:
        print_plants_menu()
        giv_input = input("Choice: ")
        print("\n")
        if giv_input == "1":
            plant.add_plant()
        elif giv_input == "2":
            plant.get_all_plants()
        elif giv_input == "3":
            plant.get_single_plant()
        elif giv_input == "4":
            plant.modify_plant()
        elif giv_input == "5":
            plant.delete_plant()
        elif giv_input == "6":
            break
        else:
            print("Invalid option: {}".format(giv_input))

def plantsgen_menu():
    ''' Controls general plants related actions'''
    genPlant = Specie()
    while True:
        print_general_plants_menu()
        giv_input = input("Choice: ")
        print("\n")
        if giv_input == "1":
            genPlant.add_general_plant()
        elif giv_input == "2":
            genPlant.get_all_general_plants()
        elif giv_input == "3":
            genPlant.get_single_general_plant()
        elif giv_input == "4":
            genPlant.modify_general_plant()
        elif giv_input == "5":
            genPlant.delete_general_plant()
        elif giv_input == "6":
            break
        else:
            print("Invalid option: {}".format(giv_input))

def diary_menu():
    ''' Controls diary related actions'''
    diary = Diary()
    while True:
        print_diary_menu()
        giv_input = input("Choice: ")
        print("\n")
        if giv_input == "1":
            diary.add_entry()
        elif giv_input == "2":
            diary.get_all_entries()
        elif giv_input == "3":
            diary.delete_entry()
        elif giv_input == "4":
            break
        else:
            print("Invalid option: {}".format(giv_input))

def print_welcome():
    print("1. Plants")
    print("2. General plants")
    print("3. Diary")
    print("4. Quit\n")

def print_plants_menu():
    print("1. Add plant")
    print("2. List all plants")
    print("3. Show plant's detailed information")
    print("4. Modify plant information")
    print("5. Delete existing plant")
    print("6. Go back to main menu\n")

def print_general_plants_menu():
    print("1. Add general plant")
    print("2. List all general plants")
    print("3. Show general plant's detailed information")
    print("4. Modify general plant information")
    print("5. Delete existing general plant")
    print("6. Go back to main menu\n")

def print_diary_menu():
    print("1. Add diary entry")
    print("2. Show diary")
    print("4. Delete existing diary entry")
    print("5. Go back to main menu\n")

if __name__ == "__main__":
    main()
