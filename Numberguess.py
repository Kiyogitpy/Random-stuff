import time
import random
import PySimpleGUI as sg
import keyboard
import math

list2 = list(range(1,1001))
Random_number = random.randint(list2[0],list2[-1])
print(Random_number)

layout = [[sg.Text(font=('Helvetica', 40), justification='left', key='text', text_color="Green"), sg.Button("Retry", button_color="red", visible=False, key="button1", enable_events=True)],
            [sg.Text('Guess the number 1-1000', justification="Center", key="text3")],[sg.Text('Enter a number', key="text2"), sg.InputText(key="-GUESS-")],
            [sg.Text('Leaderboard!',font=("Helvetica", 15), justification="Center", key="leaderboard")],]


def readLeader():
    with open('leaderboard.txt', "r") as Leadertxt:
        data = Leadertxt.read()
        # Remove leading and trailing whitespace and split by newline to get lines
        lines = data.strip().split('\n')

        # List to store tuples
        tuples = []

        # For each line, split by whitespace and convert into a tuple, then add to list
        for line in lines:
            tuples.append(tuple(line.split()))
        tuples.sort(key=lambda x: x[1], reverse=True)
        for object in tuples:
            layout.append([sg.Text(object[0] + " " + object[1],font=("Helvetica", 15), justification="Center",)],)
        
	    

readLeader()  

window = sg.Window('Running Timer', layout, auto_size_buttons=False, keep_on_top=True, grab_anywhere=True)

# ----------------  main loop  ----------------
elapsed_time = 0
start_time = int(round(time.time() + 60))
leaderboard_table = []
winner = False
saved_time = False



def hotkey_pressed(e):
    global winner
    global start_time
    global saved_time

    User_input = values["-GUESS-"]
    if not winner:
        try:
            guess = int(User_input)
            if guess == Random_number:
                window['text2'].update("You win! Enter name to add it to the leaderboard.")
                winner = True
            elif guess < Random_number: 
                window['text2'].update("Higher, Try again")
            elif guess > Random_number:
                window['text2'].update("Lower, Try again")
            window["-GUESS-"].update("")  # Clear the input text
        except ValueError:
            print("please enter a number")
    else:  # if the game is won, we're expecting the user to input their name instead of a guess
        if User_input:
            with open('leaderboard.txt', "a+") as Leadertxt:
                    Leadertxt.write(User_input + " " + win_time + "\n")
                    readLeader()  
            window["-GUESS-"].update("")  # Clear the input text
            start_time = int(round(time.time() + 60))
            window["text"].update(text_color="Green")
            window["button1"].update(visible=False)
            window['text2'].update("Write a number")
            winner = False
            saved_time = False
            window.read()
            
keyboard.on_press_key('enter', hotkey_pressed)

while (True):
    event, values = window.read(timeout=50)
    elapsed_time = int(round(time.time()))
    remaining_time = start_time - elapsed_time
    

    if remaining_time > 0 and not winner:
        window['text'].update('{:02d}:{:02d}.{:02d}'.format((remaining_time // 100) // 60,
                                                                (remaining_time // 100) % 60,
                                                                remaining_time % 100))
    elif saved_time == False and winner:
        win_time = '{:02d}:{:02d}.{:02d}'.format((remaining_time // 100) // 60,(remaining_time // 100) % 60,remaining_time % 100)
        saved_time = True
    
    if remaining_time == 40 and not winner:
        window["text"].update(text_color="Yellow")  # Clear the input text
    elif remaining_time == 20 and not winner:
        window["text"].update(text_color="Red")  # Clear the input text
    elif remaining_time == 0 and not winner:
        window["text"].update("Game Over!")
        window["button1"].update(visible=True)
        
    if event == "button1":
        start_time = int(round(time.time() + 60))
        window["text"].update(text_color="Green")
        window["button1"].update(visible=False)
        window['text2'].update("Write a number")
        winner = False

    if event == sg.WIN_CLOSED:
        break



window.close()

keyboard.unhook_all()  # Ensure to remove the hotkey hook
