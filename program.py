import tkinter
import game
import settings
import animation


class Program:
    BOARD_SIZE = 1000
    PADDING = 50
    OFFSET = 300
    COLORS = {0: "#f0483c", 1: "#4b68bf", 2: "#FFE347", 3: "#329c59",
              'click': 'indian red'}
    RADIUS = 20

    FONT20 = ("Fixedsys", 20)
    FONT40 = ("Fixedsys", 40)

    root = tkinter.Tk()
    root.resizable(0, 0)
    root.title("Dots and Boxes by Silvia Bieliková")

    canvas = None

    def __init__(self):
        try:
            if Program.canvas is None:
                Program.canvas = tkinter.Canvas(self.root, bg='white',
                                                width=self.BOARD_SIZE,
                                                height=self.BOARD_SIZE - self.OFFSET)
                self.canvas.pack()
            else:
                self.canvas.delete('all')

            self.settings = None
            self.number_of_players = None
            self.number_of_boxes = None
            self.singleplayer = None
            self.level = None

            self.game = None

            self.gap = None

            self.g_dots = []
            self.restart_button = None
            self.player_announcer = None
            self.player_scores = None
            self.pawn_background = None
            self.pawn = None
            self.pulsing_dot = None

            self.start_dot = None
            self.is_drawing = False
            self.line = None

            self.new_game()
            tkinter.mainloop()

        except tkinter.TclError:
            quit()

    def new_game(self, button=None):
        self.canvas.delete('all')
        if button is not None:
            button.destroy()

        # set up game variables from the setting screens
        self.settings = settings.Settings(self.canvas)
        self.number_of_players = self.settings.number_of_players
        self.number_of_boxes = self.settings.number_of_boxes
        self.singleplayer = self.settings.singleplayer
        self.level = self.settings.level

        self.game = game.Game(self.number_of_boxes, self.number_of_players,
                              self.singleplayer, self.level)

        self.gap = (self.BOARD_SIZE - (
                2 * self.PADDING + self.OFFSET)) / self.number_of_boxes

        # create play board
        self.g_dots = []
        self.init_board()
        self.draw_play_board()

        # create scoreboard
        self.draw_score_board()

        self.restart_button = tkinter.Button(text="RESTART",
                                             command=lambda: self.new_game(
                                                 self.restart_button),
                                             height=2, width=8, bg="indian "
                                                                   "red",
                                             activebackground=self.COLORS[
                                                 'click'],
                                             relief=tkinter.RIDGE)
        self.restart_button.place(x=self.BOARD_SIZE - self.OFFSET + 5, y=18)

        self.pulsing_dot = animation.Animation(0, 0, self.canvas, "pulse.gif")

        # bind mouse events to make moves
        self.bind_events()

        # move, mouse - variables
        self.start_dot = None
        self.is_drawing = False
        self.line = None

    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.click)
        self.canvas.bind('<Motion>', self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.drop)

    def click(self, e):
        gdot = self.is_in_dot(e.x, e.y)
        if gdot:
            self.start_dot = gdot
            self.is_drawing = True
            self.start_dot.is_clicked(self.is_drawing,
                                      self.game.current_player.id)

            fill = self.COLORS[self.game.current_player.id]
            self.line = self.canvas.create_line(gdot.x, gdot.y, gdot.x, gdot.y,
                                                width=10, fill=fill)

    def drag(self, e):
        if self.line and self.is_drawing:
            self.canvas.coords(self.line, self.start_dot.x, self.start_dot.y,
                               e.x, e.y)

    def drop(self, e):
        end_dot = self.is_in_dot(e.x, e.y)

        if self.start_dot:
            if end_dot:
                # if game is over
                if self.game.move(self.start_dot.dot, end_dot.dot):
                    self.pulsing_dot.stop()
                    self.pawn.stop()
                    self.game_over_screen()
                self.change_player_graphics()
                self.change_player_scores()

            self.canvas.delete(self.line)
            self.is_drawing = False

            self.start_dot.is_clicked(self.is_drawing,
                                      self.game.current_player.id)
            self.start_dot = None

    def is_in_dot(self, x, y):
        for item in self.g_dots:
            if ((item.x - x) ** 2 + (item.y - y) ** 2) ** (
                    1 / 2) <= self.RADIUS:
                self.canvas.coords(self.pulsing_dot.image, item.x, item.y)
                self.pulsing_dot.show()
                return item
        return None

    def init_board(self):
        for dot in self.game.dots:
            x = self.PADDING + self.gap * dot.pos_x
            y = self.PADDING + self.gap * dot.pos_y
            gdot = GDot(x, y, None, dot, self.canvas)
            self.g_dots.append(gdot)
            dot.widget = gdot

    def draw_score_board(self):
        xstart, ystart = self.BOARD_SIZE - self.OFFSET, 0
        xend, yend = self.BOARD_SIZE, self.BOARD_SIZE - self.OFFSET
        xmiddle = xstart + self.OFFSET // 2
        ys = list(range(0, yend + 1, 100))
        currentcolor = self.COLORS[self.game.current_player.id]

        # create the board
        self.canvas.create_rectangle(self.BOARD_SIZE - self.OFFSET, 0,
                                     self.BOARD_SIZE,
                                     self.BOARD_SIZE - self.OFFSET,
                                     fill="beige", outline="")

        # name of the game
        self.canvas.create_text(xmiddle, ys[1], text="DOTS\nAND\nBOXES",
                                font=self.FONT40, justify="center")

        # which player's turn it is
        text = f"{self.game.current_player.name},\nIT'S YOUR TURN"
        self.player_announcer = self.canvas.create_text(xmiddle,
                                                        (ys[4] + ys[5]) // 2,
                                                        text=text,
                                                        font=self.FONT20,
                                                        justify="center")

        # players' scores
        self.player_scores = self.canvas.create_text(xmiddle, ys[3], text="",
                                                     font=self.FONT20,
                                                     justify="right")
        self.change_player_scores()

        # dancing pawn and its background
        self.pawn_background = self.canvas.create_rectangle(xmiddle - 30, ys[5],
                                                            xmiddle + 30,
                                                            ys[7] - 20,
                                                            fill=currentcolor,
                                                            outline="")
        self.pawn = animation.Animation(xmiddle, ys[6] + 10, self.canvas,
                                        "figure.gif")
        self.pawn.show()

    # changes player announcer and pawn's background according to current player
    def change_player_graphics(self):
        text = f"{self.game.current_player.name},\nIT'S YOUR TURN"
        self.canvas.itemconfig(self.player_announcer, text=text)
        self.canvas.itemconfig(self.pawn_background,
                               fill=self.COLORS[self.game.current_player.id])

    # updates scoreboard
    def change_player_scores(self):
        output = ""
        for player in self.game.players.values():
            output += f"{player.name}: {player.score}\n"
        self.canvas.itemconfig(self.player_scores, text=output)

    def draw_play_board(self):
        self.draw_boxes()
        self.draw_lines()
        self.draw_dots()

    def draw_dots(self):
        i = 0
        for g_dot in self.g_dots:
            g_dot.object = self.canvas.create_oval(g_dot.x - self.RADIUS,
                                                   g_dot.y - self.RADIUS,
                                                   g_dot.x + self.RADIUS,
                                                   g_dot.y + self.RADIUS,
                                                   fill="white", width=2)
            self.game.dots[i].widget = g_dot
            i += 1

    # draws transparent boxes
    def draw_boxes(self):
        for box in self.game.boxes:
            dp = self.g_dots[box.leading_dot]
            x = dp.x
            y = dp.y
            obj = self.canvas.create_rectangle(x + 10, y + 10,
                                               x + self.gap - 10,
                                               y + self.gap - 10,
                                               outline='')
            box.widget = GBox(obj, self.canvas)

    # draws transparent lines
    def draw_lines(self):
        for dots in self.game.lines.keys():
            d1, d2 = dots
            d1 = self.g_dots[d1]
            d2 = self.g_dots[d2]
            self.game.lines[dots].widget = GLine(
                self.canvas.create_line(d1.x, d1.y, d2.x, d2.y, width=10,
                                        fill=''),
                self.canvas)

    def game_over_screen(self):
        coords = (2 * self.PADDING, 2 * self.PADDING,
                  self.BOARD_SIZE - 2 * self.PADDING,
                  self.BOARD_SIZE - self.OFFSET - 2 *
                  self.PADDING)
        self.canvas.create_rectangle(coords, fill="white", outline="",
                                     stipple="gray75")

        output = f"GAME OVER\n"
        number_of_winners = len(self.game.winner)
        if number_of_winners > 1:
            output += "TIE BETWEEN\n"
            output += ", ".join([str(x.name) for x in self.game.winner])
        else:
            output += f"AND THE WINNER\n IS {self.game.winner[0].name}"

        self.canvas.create_text(self.BOARD_SIZE // 2,
                                (self.BOARD_SIZE - self.OFFSET) // 2,
                                font=self.FONT40,
                                text=output, justify="center")

        # "new game" button
        g = tkinter.Button(text="PLAY AGAIN", command=lambda: self.new_game(g),
                           height=5, width=20, bg="beige", activebackground=
                           self.COLORS['click'], relief=tkinter.RIDGE)
        g.place(x=self.BOARD_SIZE // 2 - 80, y=self.BOARD_SIZE // 2)
        self.restart_button.destroy()


class GBase:
    def __init__(self, obj, canvas):
        self.object = obj
        self.canvas = canvas

    def update_graphics(self, player):
        self.canvas.itemconfig(self.object, fill=Program.COLORS[player])


class GLine(GBase):
    pass
    # everything is in super


class GBox(GBase):
    pass
    # everything is in super


class GDot(GBase):
    def __init__(self, x, y, obj, dot, canvas):
        super().__init__(obj, canvas)
        self.x = x
        self.y = y
        self.dot = dot

    def is_clicked(self, isdrawing, player):
        if isdrawing:
            color = Program.COLORS[player]
        else:
            color = "white"
        self.canvas.itemconfig(self.object, fill=color)


Program()
