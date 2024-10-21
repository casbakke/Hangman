# import modules
import tkinter as tk
from os import path
import json, random

#------------------------#

# open word list file
with open("words.json") as f:
    words_dict = json.load(f)

# define color presets
white = "#ffffff"
offwhite = "#ebebeb"
gray = "#d5d5d5"
black = "#000000"
green = "#3ade37"
red = "#de3a37"

# configure Tk window
window = tk.Tk()
window.title("Hangman")
window.configure(bg = white)
window.geometry("1280x720+120+50")
window.minsize(width = 1280, height = 720)
window.maxsize(width = 1280, height = 720)

# declare image presets
hangman0 = tk.PhotoImage(file = path.join("images", "phillip (1).png"))
hangman1 = tk.PhotoImage(file = path.join("images", "phillip (1).png"))
hangman2 = tk.PhotoImage(file = path.join("images", "phillip (1).png"))
hangman3 = tk.PhotoImage(file = path.join("images", "phillip (1).png"))
hangman4 = tk.PhotoImage(file = path.join("images", "phillip (1).png"))
hangman5 = tk.PhotoImage(file = path.join("images", "phillip (1).png"))
hangman6 = tk.PhotoImage(file = path.join("images", "phillip (1).png"))

#------------------------#

def convert_to_hangman(word, found_letters): # converts the word into the displayed text with underscores
    global running
    output = ""
    for x in range(len(word)): # for each letter in the word
        if word[x] != " ":
            if ((word[x] in found_letters) or (word[x].lower() in found_letters)) or not running:
                output += word[x]
            else:
                output += "_"
        else:
            output += " "
        if x != (len(word) - 1):
            output += " "
    return output

#----------#

def homescreen(): # screen that displays at the start of the program

    # frame widgets
    frm_head = tk.Frame(
        window,
        bg = offwhite,
    )
    
    frm_body = tk.Frame(
        window,
        bg = white,
    )

    frm_buttons = tk.Frame(
        frm_body,
        bg = offwhite,
    )

    # frame config
    window.rowconfigure(0, minsize = 140)
    window.rowconfigure(1, minsize = 580)
    window.columnconfigure(0, minsize = 1280)
    frm_body.columnconfigure(0, minsize = 1280)
    frm_head.columnconfigure(0, minsize = 1280)

    frm_head.grid(row = 0, column = 0, sticky = "nesw")
    frm_body.grid(row = 1, column = 0, sticky = "nesw")
    frm_buttons.grid(row = 0, column = 0, pady = 150)

    # widgets
    lbl_title = tk.Label(
        frm_head,
        text = "Hangman",
        font = ("Caveat", 54),
        bg = offwhite,
    )

    lbl_subtitle = tk.Label(
        frm_head,
        text = "Bacne Game Studios ©2022",
        font = ("Ariel", 18),
        bg = offwhite,
    )

    btn_singleplayer = tk.Button(
        frm_buttons,
        text = "Start Game",
        font = ("Ariel", 30),
        width = 14,
        command = category_select,
        background = gray,
        activebackground = gray,
    )

    # widget config
    lbl_title.grid(row = 0, column = 0)
    lbl_subtitle.grid(row = 1, column = 0)

    btn_singleplayer.grid(row = 0, column = 0, padx = 25, pady = 25, ipady = 15)

#----------#

def gamescreen(word, hint): # screen that displays when actively playing hangman
    clear()
    global level
    level = 0 # user's "lives" or guesses remaining (counts up to 6)
    found_letters = [] # list of correct letters that have been clicked
    global running
    running = True

    # event handlers
    def hangman_increase(): # decreases the user's "lives" and switches the hangman image
        global level
        level += 1
        img_hangman["image"] = eval(f"hangman{level}")

    def game_won(): # when the user wins the game
        global running
        running = False
        lbl_hint["text"] = "You Win!"
        btn_home.place(x = 1015, y = 18)

    def game_lost(): # when the user loses the game
        global running
        running = False
        lbl_hint["text"] = "You Lost"
        lbl_word["text"] = convert_to_hangman(word, found_letters)
        btn_home.place(x = 1015, y = 18)

    def letter_clicked(letter): # when the user presses a key or clicks a letter
        if (eval(f"btn_{letter}")["bg"] == gray) and running: # if the letter hasn't been clicked and the game is running
            if (letter in word) or (letter.upper() in word): # if the letter is in the word
                eval(f"btn_{letter}")["bg"] = green
                eval(f"btn_{letter}")["activebackground"] = green
                found_letters.append(letter) # add the letter to the list of found letters
                lbl_word["text"] = convert_to_hangman(word, found_letters)
                if not "_" in lbl_word["text"]: # if the entire word has been found
                    game_won()
            else: # if the letter is not in the word
                eval(f"btn_{letter}")["bg"] = red
                eval(f"btn_{letter}")["activebackground"] = red
                hangman_increase() # decrease user's remaining guesses
                if level == 6: # if the user has used all of their guesses
                    game_lost()

    # frame widgets
    frm_head = tk.Frame(
        window,
        bg = offwhite,
    )
    
    frm_body = tk.Frame(
        window,
        bg = white,
    )

    # frame config
    window.rowconfigure(0, minsize = 100)
    window.rowconfigure(1, minsize = 620)
    window.columnconfigure(0, minsize = 1280)
    frm_body.columnconfigure(0, minsize = 1280)
    frm_head.columnconfigure(0, minsize = 1280)

    frm_head.grid(row = 0, column = 0, sticky = "nesw")
    frm_body.grid(row = 1, column = 0, sticky = "nesw")
    
    # widgets
    lbl_hint = tk.Label(
        frm_head,
        text = hint,
        font = ("Arial", 48),
        bg = offwhite,
    )
    
    img_hangman = tk.Label(
        frm_body,
        image = hangman0,
        bg = white,
    )

    frm_word = tk.Frame(
        frm_body,
        bg = black
    )

    frm_letters = tk.Frame(
        frm_body,
        bg = offwhite,
    )

    lbl_word = tk.Label(
        frm_word,
        text = convert_to_hangman(word, found_letters),
        bg = white,
        font = ("Ariel", 26),
        width = 36,
    )

    # frame config
    lbl_hint.grid(row = 0, column = 0, pady = (10, 0))
    img_hangman.place(x = 20, y = 70)
    frm_word.place(x = 500, y = 150)
    lbl_word.grid(row = 0, column = 0, ipady = 5, padx = 3, pady = 3)
    frm_letters.place(x = 550, y = 280)

    # all the letters in the alphabet, in an ordered list
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    global btn_a, btn_b, btn_c, btn_d, btn_e, btn_f, btn_g, btn_h, btn_i, btn_j, btn_k, btn_l, btn_m, btn_n, btn_o, btn_p, btn_q, btn_r, btn_s, btn_t, btn_u, btn_v, btn_w, btn_x, btn_y, btn_z

    # declare buttons
    btn_a = tk.Button(frm_letters, command = lambda: letter_clicked("a"))
    btn_b = tk.Button(frm_letters, command = lambda: letter_clicked("b"))
    btn_c = tk.Button(frm_letters, command = lambda: letter_clicked("c"))
    btn_d = tk.Button(frm_letters, command = lambda: letter_clicked("d"))
    btn_e = tk.Button(frm_letters, command = lambda: letter_clicked("e"))
    btn_f = tk.Button(frm_letters, command = lambda: letter_clicked("f"))
    btn_g = tk.Button(frm_letters, command = lambda: letter_clicked("g"))
    btn_h = tk.Button(frm_letters, command = lambda: letter_clicked("h"))
    btn_i = tk.Button(frm_letters, command = lambda: letter_clicked("i"))
    btn_j = tk.Button(frm_letters, command = lambda: letter_clicked("j"))
    btn_k = tk.Button(frm_letters, command = lambda: letter_clicked("k"))
    btn_l = tk.Button(frm_letters, command = lambda: letter_clicked("l"))
    btn_m = tk.Button(frm_letters, command = lambda: letter_clicked("m"))
    btn_n = tk.Button(frm_letters, command = lambda: letter_clicked("n"))
    btn_o = tk.Button(frm_letters, command = lambda: letter_clicked("o"))
    btn_p = tk.Button(frm_letters, command = lambda: letter_clicked("p"))
    btn_q = tk.Button(frm_letters, command = lambda: letter_clicked("q"))
    btn_r = tk.Button(frm_letters, command = lambda: letter_clicked("r"))
    btn_s = tk.Button(frm_letters, command = lambda: letter_clicked("s"))
    btn_t = tk.Button(frm_letters, command = lambda: letter_clicked("t"))
    btn_u = tk.Button(frm_letters, command = lambda: letter_clicked("u"))
    btn_v = tk.Button(frm_letters, command = lambda: letter_clicked("v"))
    btn_w = tk.Button(frm_letters, command = lambda: letter_clicked("w"))
    btn_x = tk.Button(frm_letters, command = lambda: letter_clicked("x"))
    btn_y = tk.Button(frm_letters, command = lambda: letter_clicked("y"))
    btn_z = tk.Button(frm_letters, command = lambda: letter_clicked("z"))

    # when a key is pressed, call the corresponding function
    def key_pressed(event):
        letter_clicked(event.char)

    for letter in letters:
        window.bind(letter, key_pressed)

    # draw the keyboard
    for row in range(3):
        for col in range(9):
            try:
                letter = letters[row * 9 + col].lower()
            except:
                break
            button = eval(f"btn_{letter}")
            button["width"] = 1
            button["text"] = letter.upper()
            button["font"] = ("Ariel", 24)
            button["bg"] = gray
            button["activebackground"] = gray
            button.grid(row = row, column = col, padx = 4, pady = 4, ipadx = 16)

    btn_home = tk.Button( # home button that shows after the game has finished
        frm_head,
        text = "Return to Menu",
        font = ("Arial", 24),
        bg = green,
        activebackground = green,
        command = homescreen,
    )
            
#----------#

def category_select(): # allows the player to select a category for the words or randomize it

    clear()

    # event handlers
    def cat_selected(cat):
        if cat != "Random":
            category = cat
        else:
            category = random.choice(list(words_dict.keys()))
        word = random.choice(words_dict[category])
        gamescreen(word, category)

    # frame widgets
    frm_body = tk.Frame(
        window,
        bg = offwhite,
    )

    # frame config
    window.rowconfigure(0, minsize = 720)
    window.columnconfigure(0, minsize = 1280)

    frm_body.grid(row = 0, column = 0)

    # widgets
    lbl_head = tk.Label(
        frm_body,
        text = "Choose a Category",
        font = ("Ariel", 24),
        bg = offwhite,
    )

    btn_cat0 = tk.Button(
        frm_body,
        text = "Presidents",
        font = ("Ariel", 24),
        width = 16,
        background = gray,
        activebackground = gray,
        command = lambda: cat_selected("Presidents")
    )

    btn_cat1 = tk.Button(
        frm_body,
        text = "States",
        font = ("Ariel", 24),
        width = 16,
        background = gray,
        activebackground = gray,
        command = lambda: cat_selected("States")
    )
    
    btn_cat2 = tk.Button(
        frm_body,
        text = "Food",
        font = ("Ariel", 24),
        width = 16,
        background = gray,
        activebackground = gray,
        command = lambda: cat_selected("Food")
    )

    btn_cat3 = tk.Button(
        frm_body,
        text = "Animals",
        font = ("Ariel", 24),
        width = 16,
        background = gray,
        activebackground = gray,
        command = lambda: cat_selected("Animals")
    )
    
    btn_cat4 = tk.Button(
        frm_body,
        text = "Random",
        font = ("Ariel", 24),
        width = 16,
        background = gray,
        activebackground = gray,
        command = lambda: cat_selected("Random")
    )

    # widget config
    lbl_head.grid(row = 0, column = 0, padx = 20, pady = (15, 10))
    btn_cat0.grid(row = 1, column = 0, padx = 20)
    btn_cat1.grid(row = 2, column = 0, padx = 20, pady = 3)
    btn_cat2.grid(row = 3, column = 0, padx = 20)
    btn_cat3.grid(row = 4, column = 0, padx = 20, pady = 3)
    btn_cat4.grid(row = 5, column = 0, padx = 20, pady = (0, 20))

#----------#

def clear(): # clears all widgets from the screen
    for widget in window.winfo_children():
        widget.destroy()

#------------------------#

homescreen()
window.mainloop()