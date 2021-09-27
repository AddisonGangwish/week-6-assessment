#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

bank = [0, 0, 0]
wheel = [-1, 0, 100, 150, 200, 250, 300, 350, 400, 400, 450, 450, 500, 500, 550, 550, 600, 600, 650, 700, 750, 800, 850, 900]
phrases = ["LEARNING THE METRIC SYSTEM", "PAPER AND PAPER CLIP", "WHAT IS THE ANSWER?"]
categories = ["What are you doing?", "Things", "Phrase"]
vowels = {"A", "E", "I", "O", "U"}
rstlne = {"R", "S", "T", "L", "N", "E"}


# In[2]:


def get_letters(phrase):
    letters = set()
    for letter in phrase:
        if letter.isalpha():
            letters.add(letter)
    return letters


# In[3]:


def print_standings(bank):
    print(f"Player Standings\n"
          f"================\n"
          f"Player 1: ${bank[0]}\n"
          f"Player 2: ${bank[1]}\n"
          f"Player 3: ${bank[2]}\n")


# In[4]:


def print_phrase(phrase, category, letters):
    out = ""
    for ch in phrase:
        if ch.isalpha() and ch not in letters:
            out += "_"
        else:
            out += ch
    out = out.replace("", " ")
    width = max(len(out), len(category)) + 2
    out = out.center(width)
    category = category.center(width)
    outline = "=" * width
    print(f"{outline}\n"
          f"{out}\n"
          f"{outline}\n"
          f"{category}\n"
          f"{outline}\n")


# In[5]:


def menu(choices):
    while True:
        for choice in range(1, len(choices) + 1):
            if choices[choice - 1] == "s":
                print(f"{choice}. Spin the wheel")
            elif choices[choice - 1] == "v":
                print(f"{choice}. Buy a vowel")
            elif choices[choice - 1] == "g":
                print(f"{choice}. Solve the puzzle")
            elif choices[choice - 1] == "p":
                print(f"{choice}. Pass turn")
        selection = input("\n").strip()
        if not selection.isdigit() or (int(selection) < 1 or int(selection) > len(choices)):
            print("\nError:"
                  "\nSelection must be a number from the list. Please try again.\n")
        else:
            return(choices[int(selection) - 1])


# In[6]:


for round in range(1,4):
    guessed = False
    phrase = phrases[round - 1]
    category = categories[round - 1]
    unguessed_letters = get_letters(phrase)
    guessed_letters = set()
    
    if round == 1 or round == 2:
        print(f"Round {round}\n")
        while not guessed:
            for player in range(1,4):
                if guessed:
                    break
                print_standings(bank)
                print_phrase(phrase, category, guessed_letters)
                
                print(f"Player {player}'s turn\n"
                      f"===============\n")
                if len(unguessed_letters - vowels) > 0:
                    selection = menu("s")
                    if selection == "s":
                        print("\nSpinning Wheel")
                        value = random.choice(wheel)
                        if value == -1:
                            print("Wheel landed on Bankrupt.\n")
                            bank[player - 1] = 0
                            continue
                        elif value == 0:
                            print("Wheel landed on Lose a Turn.\n")
                            continue
                        else:
                            print(f"Wheel landed on ${value}.\n")
                
                    consonant = input("\nGuess a consonant: ").strip().upper()
                    if consonant in guessed_letters:
                        print(f"'{consonant}' has already been guessed.\n")
                        continue
                    elif consonant in vowels or not consonant.isalpha():
                        print(f"'{consonant}' is not a consonant.\n")
                        continue
                    elif consonant not in unguessed_letters:
                        print(f"'{consonant}' is not in the phrase.\n")
                        guessed_letters.add(consonant)
                        continue
                    else:
                        print(f"'{consonant}' is in the phrase.\n")
                        bank[player - 1] += value
                        guessed_letters.add(consonant)
                        unguessed_letters.remove(consonant)
                        print_standings(bank)
                        print_phrase(phrase, category, guessed_letters)
                        if len(unguessed_letters) == 0:
                            print("You've completed the phrase.\n")
                            guessed = True
                            continue
                
                if len(unguessed_letters - vowels) == 0:
                    print("Only vowels remain.\n")
                
                skip = False
                if len(unguessed_letters & vowels) > 0 and bank[player - 1] >= 250:
                    vgp = True
                    while vgp:
                        if bank[player - 1] < 250:
                            break
                        selection = menu("vgp")
                        if selection == "v":
                            bank[player - 1] -= 250
                            vowel = input("\nBuy a vowel: ").strip().upper()
                            if vowel in guessed_letters:
                                print(f"'{vowel}' has already been guessed.\n")
                            elif vowel not in vowels or not vowel.isalpha():
                                print(f"'{vowel}' is not a vowel.\n")
                            elif vowel not in unguessed_letters:
                                print(f"'{vowel}' is not in the phrase.\n")
                                guessed_letters.add(vowel)
                            else:
                                print(f"'{vowel}' is in the phrase.\n")
                                guessed_letters.add(vowel)
                                unguessed_letters.remove(vowel)
                                print_standings(bank)
                                print_phrase(phrase, category, guessed_letters)
                                if len(unguessed_letters) == 0:
                                    print("You've completed the phrase.")
                                    guessed = True
                                else:
                                    if len(unguessed_letters & vowels) == 0:
                                        print("No vowels remaining.\n")
                                        break
                                    else:
                                        continue
                        elif selection == "p":
                            print("\nPassing Turn\n")
                        else:
                            skip = True
                            break
                        vgp = False
                    else:
                        continue
                else:
                    if len(unguessed_letters & vowels) == 0:
                        print("No vowels remaining.\n")
                
                if not skip:
                    selection = menu("gp")
                    if selection == "p":
                        print("\nPassing Turn")
                        continue
                
                guess = input("\nGuess the phrase: ").strip().upper()
                if guess == phrase:
                    print("You guessed the phrase.\n")
                    guessed = True
                    break
                else:
                    print(f"'{guess}' is not the phrase.\n")
                        
    if round == 3:
        print(f"Final Round\n")
        player = bank.index(max(bank)) + 1
        print(f"Player {player} gets to play.\n")
        unguessed_letters = unguessed_letters - rstlne
        guessed_letters.update(rstlne)
        print_phrase(phrase, category, guessed_letters)
        
        for i in range(1, 4):
            while True:
                consonant = input(f"Enter consonant #{i}: ").strip().upper()
                if consonant in guessed_letters:
                    print(f"{consonant} has already been guessed. Try again.\n")
                elif consonant.isalpha() and consonant not in vowels:
                    unguessed_letters.discard(consonant)
                    guessed_letters.add(consonant)
                    break
                else:
                    print(f"{consonant} is not a consonant. Try again.\n")
        while True:
            vowel = input(f"Enter vowel: ").strip().upper()
            if vowel in vowels:
                if vowel in guessed_letters:
                    print(f"{vowel} has already been guessed. Try again.\n")
                elif vowel.isalpha():
                    unguessed_letters.discard(vowel)
                    guessed_letters.add(vowel)
                    break
            else:
                print(f"{vowel} is not a vowel. Try again.\n")
                
        print_phrase(phrase, category, guessed_letters)
        guess = input("Guess the phrase: ").strip().upper()
        if guess == phrase:
            print(f"You guessed it!\n"
                  f"Player {player} has won ${bank[player - 1]}!")
        else:
            print(f"You lost. The phrase was: '{phrase}'")


# # 
