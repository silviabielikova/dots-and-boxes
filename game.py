import random


class Game:
    def __init__(self, n, players, singleplayer, level):
        self.singleplayer = singleplayer
        self.level = level
        self.number_of_players = players
        self.number_of_boxes = n
        self.number_of_lines = 2 * self.number_of_boxes * (
                self.number_of_boxes + 1)

        self.game_over = False
        self.played_moves = 0

        # creates logical board
        self.dots = []
        self.lines = {}
        self.free_lines = set()
        self.boxes = []
        self.create_grid()

        # creates players dictionary, keys are their index numbers
        self.players = {}
        if self.singleplayer:
            self.players[0] = Player(0)
            self.players[1] = AIPlayer(1)
            self.current_player = self.players[0]
        else:
            for i in range(self.number_of_players):
                self.players[i] = Player(i)

            # randomly sets whose turn its is to start
            random_player = random.randint(0, self.number_of_players - 1)
            self.current_player = self.players[random_player]

        self.winner = None

    # creates grid: dots, boxes, relations between them
    def create_grid(self):
        index = 0
        m = self.number_of_boxes + 1
        for i in range(m ** 2):
            d = Dot(index, self.number_of_boxes)
            self.create_paths(d, self.number_of_boxes + 1)
            self.dots.append(d)
            index += 1
        self.create_boxes()

    # decides all possible paths = where lines can be drawn
    def create_paths(self, dot, m):
        dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for d in dirs:
            neighbor = [dot.pos_x + d[0], dot.pos_y + d[1]]
            if (0 <= neighbor[0] < m) and (0 <= neighbor[1] < m):
                n = neighbor[1] * m + neighbor[0]
                a = tuple(sorted((dot.id, n)))
                self.lines[a] = Line()
                self.free_lines.add(a)

    # creates list of boxes, lines get their adjacent boxes
    def create_boxes(self):
        for i in range(self.number_of_boxes ** 2):
            self.boxes.append(Box(i, self.number_of_boxes, self.lines))
        for box in self.boxes:
            self.lines[box.top_dots].boxes.append(box)
            self.lines[box.right_dots].boxes.append(box)
            self.lines[box.bottom_dots].boxes.append(box)
            self.lines[box.left_dots].boxes.append(box)

    # single move in the game
    def move(self, d1, d2):
        if self.game_over:
            return self.game_over
        filled = False
        a = tuple(sorted((d1.id, d2.id)))
        if a in self.lines:
            if self.lines[a].owner is None:
                # line gets its owner
                self.lines[a].owner = self.current_player
                self.free_lines.remove(a)
                self.lines[a].widget.update_graphics(self.current_player.id)
                self.played_moves += 1
                # checks line's adjacent boxes, sets their owner if became full
                for box in self.lines[a].boxes:
                    if box.is_full:
                        box.widget.update_graphics(self.current_player.id)
                        filled = True
                        box.owner = self.current_player
                        self.current_player.add_score()
                        # and player gets another move
                # no box was filled during this move
                if not filled:
                    # the next player is on the move
                    self.current_player = self.get_next_player()

        # checks if game is still in progress
        if self.played_moves < self.number_of_lines:
            self.game_over = False
            # lets the computer play a move
            if type(self.current_player) == AIPlayer:
                self.computer_move()
        else:
            self.game_over = True
            self.set_winner()
        return self.game_over

    def get_3_edged_box_line(self):
        for box in self.boxes:
            edges = [(box.top_line, box.top_dots), (box.right_line,
                                                    box.right_dots),
                     (box.bottom_line, box.bottom_dots),
                     (box.left_line, box.left_dots)]
            not_owned = [edge for edge in edges if edge[0].owner is None]
            if len(not_owned) == 1:
                dots = not_owned[0][1]
                return dots[0], dots[1]
        return None

    def get_unsafe_lines(self):
        unsafe_lines = set()
        for box in self.boxes:
            edges = [(box.top_line, box.top_dots), (box.right_line,
                                                    box.right_dots),
                     (box.bottom_line, box.bottom_dots),
                     (box.left_line, box.left_dots)]
            not_owned = [edge for edge in edges if edge[0].owner is None]
            if len(not_owned) == 2:
                unsafe_lines.add(not_owned[0][1])
                unsafe_lines.add(not_owned[1][1])
        return unsafe_lines

    def computer_move(self):
        # level 1 difficulty
        # random moves, easy to beat
        if self.level == 1:
            if self.free_lines != set():
                line = random.choice(list(self.free_lines))

        # level 2 difficulty
        # always adds the 4th line, doesn't let the opponent score = never
        # adds the third line
        # random move only if both not possible
        elif self.level == 2:
            line = self.get_3_edged_box_line()
            if line is None:
                unsafe_lines = self.get_unsafe_lines()
                if self.free_lines != set():
                    movable = self.free_lines - unsafe_lines
                    if movable != set():
                        line = random.choice(list(movable))
                    else:
                        line = random.choice(list(self.free_lines))

        # level 3 difficulty
        # similar to level 2 but with added backtracking when scoring is not
        # possible = finds the minimum loss = opponent's lowest gain
        else:
            results = []

            # simulation of opponent's ("ideal") streak after letting them score

            def backtracking(start_line, streak_cnt):
                line = self.get_3_edged_box_line()
                if line is None:
                    results.append((streak_cnt, start_line))
                else:
                    self.lines[line].owner = "BT"
                    backtracking(start_line, streak_cnt + 1)
                    self.lines[line].owner = None

            line = self.get_3_edged_box_line()
            if line is None:
                unsafe_lines = self.get_unsafe_lines()
                if self.free_lines != set():
                    movable = self.free_lines - unsafe_lines
                    if movable != set():
                        line = random.choice(list(movable))
                    # evaluates all "3rd line" moves
                    else:
                        for l in self.free_lines:
                            self.lines[l].owner = "BT"
                            backtracking(l, 0)
                            self.lines[l].owner = None
                        min_streak = None
                        # decides next move based on opponent's following streak
                        # = finds the shortest streak
                        for streak_cnt, l in results:
                            if min_streak is None or streak_cnt < min_streak:
                                min_streak = streak_cnt
                                line = l
        # performs the move
        dots = [self.dots[i] for i in line]
        self.move(*dots)

    # returns the next player
    def get_next_player(self):
        return self.players[
            (self.current_player.id + 1) % self.number_of_players]

    # checks individual scores and returns winners in a list
    def set_winner(self):
        w = None
        for player in self.players.values():
            if w is None:
                w = [player]
            else:
                if player.score > w[0].score:
                    w = [player]
                elif player.score == w[0].score:
                    w.append(player)
        self.winner = w


class Player:
    def __init__(self, i):
        self.id = i
        self.score = 0

    def add_score(self):
        self.score += 1

    # player id incremented to feel more natural in a game
    @property
    def name(self):
        return f"PLAYER {self.id + 1}"


class AIPlayer(Player):
    @property
    def name(self):
        return "THE COMPUTER"


class Dot:
    def __init__(self, i, n):
        m = n + 1
        self.id = i

        self.pos_y = i // m
        self.pos_x = i % m

        # its visible object, will set in Program when drawing the board
        self.widget = None


class Box:
    # i is index of the dot in the top left corner of the box
    def __init__(self, i, n, lines):
        self.id = i
        self.owner = None

        d = i + i // n
        self.leading_dot = d

        self.top_dots = tuple(sorted((d, d + 1)))
        self.top_line = lines[self.top_dots]
        d += 1
        self.right_dots = tuple(sorted((d, d + 1 + n)))
        self.right_line = lines[self.right_dots]
        d += 1 + n
        self.bottom_dots = tuple(sorted((d, d - 1)))
        self.bottom_line = lines[self.bottom_dots]
        d -= 1
        self.left_dots = tuple(sorted((d, d - 1 - n)))
        self.left_line = lines[self.left_dots]

        self.widget = None

    # checks if all of the adjacent lines have owner, decides if is full
    @property
    def is_full(self):
        return (self.top_line.owner and self.right_line.owner and
                self.bottom_line.owner and self.left_line.owner)


class Line:
    def __init__(self):
        self.owner = None
        self.boxes = []

        self.widget = None
