import tkinter
from tkinter import font
import json


class Settings:
    FONT20 = ("Fixedsys", 20)
    FONT40 = ("Fixedsys", 40)
    Y1, Y2, Y3 = 150, 400, 600
    BUTTON_CLICK = 'indian red'
    BUTTON_DEFAULT = 'beige'

    def __init__(self, canvas):
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Fixedsys")

        # no value until is set
        self.number_of_players = None
        self.number_of_boxes = None
        self.singleplayer = None
        self.level = None

        # lists of buttons used
        self.buttons1 = []
        self.ps = []
        self.ns = []

        self.canvas = canvas

        # let the players choose
        try:
            self.choose_settings()
        except tkinter.TclError:
            quit()

    # changes buttons' colors according to chosen settings
    def update_buttons(self):
        if self.number_of_players is not None:
            for p in self.ps:
                if p['text'][0] == str(self.number_of_players):
                    p['bg'] = self.BUTTON_CLICK
                else:
                    p['bg'] = self.BUTTON_DEFAULT
        if self.level is not None:
            for p in self.ps:
                if p['text'][-1] == str(self.level):
                    p['bg'] = self.BUTTON_CLICK
                else:
                    p['bg'] = self.BUTTON_DEFAULT
        if self.number_of_boxes is not None:
            for n in self.ns:
                if n['text'][0] == str(self.number_of_boxes):
                    n['bg'] = self.BUTTON_CLICK
                else:
                    n['bg'] = self.BUTTON_DEFAULT
        self.canvas.update()

    def set_number_of_players(self, p):
        self.number_of_players = p

    def set_number_of_boxes(self, n):
        self.number_of_boxes = n

    def set_game_mode(self, sp):
        self.singleplayer = sp
        if self.singleplayer:
            self.number_of_players = 2

    def set_level(self, l):
        self.level = l

    # imports last game's settings from file
    def import_settings(self):
        my_settings = json.load(open('mysettings.txt'))
        self.number_of_players = my_settings["numberOfPlayers"]
        self.number_of_boxes = my_settings["numberOfBoxes"]
        self.singleplayer = my_settings["singleplayer"]
        self.level = my_settings["level"]

    # saves current settings to file
    def export_settings(self):
        if self.settings_complete():
            my_settings = {"numberOfPlayers": self.number_of_players,
                           "numberOfBoxes": self.number_of_boxes,
                           "singleplayer": self.singleplayer,
                           "level": self.level}
            with open('mysettings.txt', 'w') as file:
                json.dump(my_settings, file, indent=2)

    def create_button(self, text, command, height, width):
        return tkinter.Button(text=text, command=command, height=height,
                              width=width, bg=self.BUTTON_DEFAULT,
                              activebackground=self.BUTTON_CLICK,
                              relief=tkinter.RIDGE)

    def welcome_and_load(self):
        self.canvas.create_text(500, self.Y1 - 50, text="WELCOME TO DOTS AND "
                                                        "BOXES",
                                font=self.FONT40)
        # button for loading saved settings
        self.buttons1.append(self.create_button("USE MY LAST SETTINGS",
                                                self.import_settings, 5, 70))
        self.buttons1[0].place(x=200, y=self.Y2 - 150)

    # text and buttons for choosing game mode: multiplayer/singleplayer
    def choose_game_mode(self):
        self.canvas.create_text(500, self.Y3 - 150, text="GAME MODE:",
                                font=self.FONT20)

        self.buttons1.append(self.create_button("SINGLEPLAYER",
                                                lambda:self.set_game_mode(True), 5, 20))
        self.buttons1[1].place(x=200, y=self.Y3-100)

        self.buttons1.append(self.create_button("MULTIPLAYER",
                                                lambda:self.set_game_mode(False), 5, 20))
        self.buttons1[2].place(x=600, y=self.Y3-100)

    # text and buttons for setting the level of difficulty
    def choose_level(self):
        self.canvas.create_text(500, self.Y1 - 50, text="LEVEL OF DIFFICULTY:",
                                font=self.FONT20)
        for i in range(1, 4):
            self.ps.append(
                self.create_button(f"LEVEL {i}", lambda i=i: self.set_level(i),
                                   5, 20))
            self.ps[i - 1].place(x=i * 200, y=self.Y1)

    # text and buttons for setting the number of players
    def choose_number_of_players(self):
        self.canvas.create_text(500, self.Y1 - 50, text="NUMBER OF "
                                                        "PLAYERS:",
                                font=self.FONT20)
        for i in range(2, 5):
            self.ps.append(self.create_button(f"{i} PLAYERS", lambda
                i=i: self.set_number_of_players(i), 5, 20))
            self.ps[i - 2].place(x=(i - 1) * 200, y=self.Y1)

    # text and buttons for setting the number of boxes
    def choose_number_of_boxes(self):
        self.canvas.create_text(500, self.Y2 - 50, text="SIZE OF THE BOARD:",
                                font=self.FONT20)
        for i in range(2, 5):
            self.ns.append(self.create_button(f"{i}x{i}", lambda
                i=i: self.set_number_of_boxes(i), 5, 20))
            self.ns[i - 2].place(x=(i - 1) * 200, y=self.Y2)

    def save_and_update(self):
        self.update_buttons()
        self.export_settings()
        self.canvas.update()
        self.canvas.after(750)

    # destroy all buttons and texts, clean canvas
    def clear_screen(self):
        self.save_and_update()
        for button in self.buttons1 + self.ns + self.ps:
            button.destroy()
        self.canvas.delete('all')

    # is everything set properly?
    def settings_complete(self):
        if self.singleplayer is None:
            return False
        if self.singleplayer:
            return self.number_of_boxes and self.level
        return self.number_of_boxes and self.number_of_players

    def choose_settings(self):
        # welcome screen, first settings screen
        self.welcome_and_load()
        self.choose_game_mode()

        # loop until game mode is set
        while self.singleplayer is None:
            self.update_buttons()

        self.clear_screen()

        # second settings screen
        if not self.settings_complete():
            if self.singleplayer:
                self.choose_level()
            else:
                self.choose_number_of_players()
            self.choose_number_of_boxes()

            # loop until number of boxes and number of players or
            # difficulty level is set
            while not self.settings_complete():
                self.update_buttons()

            self.clear_screen()
