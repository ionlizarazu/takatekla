import gettext
import logging
import random
import re
import socket
from tkinter import END, Button, Label, Text

import config
import secret
import text

# set current language
tr = gettext.translation(
    "base", localedir="locales", languages=config.language
)
tr.install()
_ = tr.gettext
logging.basicConfig(filename="example.log", level=logging.DEBUG)


class Game(Frame):
    def __init__(
        self,
        cellW,
        cellH,
        rows,
        columns,
        master,
        mode,
        colors={"main-bg": "#146791", "disabled-bg": "#7798a8"},
    ):
        super().__init__(master)

        master.configure(background=colors["panel-bg"])
        master.title("TAKATEKLA")
        master.geometry(
            str(columns * cellW + 30 + cellW + 30)
            + "x"
            + str((rows * cellH) + 80)
        )
        self.master = master
        self.cellW = cellW
        self.cellH = cellH
        self.rows = rows
        self.columns = columns
        self.base_starting_y = 70
        self.base_starting_x = 15
        self.colors = colors
        self.to_search = ""
        self.the_list = []
        self.taka_team = {}
        self.tekla_team = {}
        self.taka_color = "tomato3"
        self.tekla_color = "deep sky blue"
        self.players = {}
        self.players_colors = [
            "deep sky blue",
            "dark turquoise",
            "medium aquamarine",
            "dark green",
            "sea green",
            "goldenrod",
            "indian red",
            "dark orange",
            "orange red",
            "violet red",
            "dark violet",
            "blue4",
            "SeaGreen3",
            "OliveDrab4",
            "IndianRed4",
            "tomato3",
        ]
        if mode == "i":
            self.init_table()
        elif mode == "t":
            self.init_teams_table()
        self.pack()
        self.create_widgets(mode)

    def init_table(self):
        # table_starting_point = 15 + self.cellW
        for i in range(self.rows):
            for j in range(self.columns):
                exec(
                    "self.e"
                    + str(i)
                    + str(j)
                    + " = Entry(self.master, bg='"
                    + self.colors["disabled-bg"]
                    + "', fg='white', font=('Arial', 22, 'bold'), justify=CENTER)"
                    # + "', fg='white', font=('Blackout', 18, 'bold'), justify=CENTER)"
                )
                exec("self.e" + str(i) + str(j) + ".grid(row=i, column=j)")
                exec(
                    "self.e"
                    + str(i)
                    + str(j)
                    + ".place(x=j*self.cellW + self.base_starting_x, y=i*self.cellH+self.base_starting_y, height=self.cellH, width=self.cellW)"
                )
                exec("self.e" + str(i) + str(j) + ".insert(END, '')")
        self.winners_label = Label(self.master, text=_("Ranking:"))
        self.winners_label.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y + 2 * self.cellH,
            width=self.cellW,
        )

        self.winners = Text(self.master)
        self.winners.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y + 20 + 2 * self.cellH,
            width=self.cellW,
            height=self.rows * self.cellH / 2 - 20,
        )

        self.allowed_players_label = Label(
            self.master, text=_("Allowed players:")
        )
        self.allowed_players_label.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y
            + (self.rows * self.cellH / 2)
            + 2 * self.cellH,
            width=self.cellW,
        )

        self.allowed_players = Text(self.master)
        self.allowed_players.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y
            + (self.rows * self.cellH / 2)
            + 20
            + 2 * self.cellH,
            width=self.cellW,
            height=self.rows * self.cellH / 2 - 20 - 2 * self.cellH,
        )

    def init_teams_table(self):
        # table_starting_point = 15 + self.cellW
        for i in range(self.rows):
            for j in range(self.columns):
                exec(
                    "self.e"
                    + str(i)
                    + str(j)
                    + " = Entry(self.master, bg='"
                    + self.colors["disabled-bg"]
                    + "', fg='white', font=('Arial', 22, 'bold'), justify=CENTER)"
                )
                exec("self.e" + str(i) + str(j) + ".grid(row=i, column=j)")
                exec(
                    "self.e"
                    + str(i)
                    + str(j)
                    + ".place(x=j*self.cellW + self.base_starting_x, y=i*self.cellH+self.base_starting_y, height=self.cellH, width=self.cellW)"
                )
                exec("self.e" + str(i) + str(j) + ".insert(END, '')")

        self.results_label = Label(self.master, text=_("Results:"))
        self.results_label.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y + 2 * self.cellH,
            width=self.cellW,
        )

        self.taka_r_label = Label(self.master, text=_("TAKA:"))
        self.taka_r_label.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y + 2 * self.cellH + 20,
            width=self.cellW / 2,
        )

        self.tekla_r_label = Label(self.master, text=_("TEKLA:"))
        self.tekla_r_label.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.cellW / 2
            + self.base_starting_x,
            y=self.base_starting_y + 2 * self.cellH + 20,
            width=self.cellW / 2,
        )

        self.taka_points = Text(self.master)
        self.taka_points.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y + 20 + 20 + 2 * self.cellH,
            width=self.cellW / 2,
            height=self.rows * self.cellH / 6 - 30,
        )
        self.taka_points.config(font=("Arial", 50, "bold"))

        self.tekla_points = Text(self.master)
        self.tekla_points.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.cellW / 2
            + self.base_starting_x,
            y=self.base_starting_y + 20 + 20 + 2 * self.cellH,
            width=self.cellW / 2,
            height=self.rows * self.cellH / 6 - 30,
        )
        self.tekla_points.config(font=("Arial", 50, "bold"))

        # self.winners = Text(self.master)
        # self.winners.place(x=self.base_starting_x + self.columns * self.cellW + self.base_starting_x,
        #                            y=self.base_starting_y + 20 + 20 + 2*self.cellH, width=self.cellW, height=self.rows * self.cellH / 4 - 20)

        self.taka_label = Label(self.master, text=_("TAKA:"))
        self.taka_label.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y
            + (self.rows * self.cellH / 2)
            + 2 * self.cellH,
            width=self.cellW / 2,
        )

        self.taka = Text(self.master)
        self.taka.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.base_starting_x,
            y=self.base_starting_y
            + (self.rows * self.cellH / 2)
            + 20
            + 2 * self.cellH,
            width=self.cellW / 2,
            height=self.rows * self.cellH / 2 - 20 - 2 * self.cellH,
        )

        self.tekla_label = Label(self.master, text=_("TEKLA:"))
        self.tekla_label.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.cellW / 2
            + self.base_starting_x,
            y=self.base_starting_y
            + (self.rows * self.cellH / 2)
            + 2 * self.cellH,
            width=self.cellW / 2,
        )

        self.tekla = Text(self.master)
        self.tekla.place(
            x=self.base_starting_x
            + self.columns * self.cellW
            + self.cellW / 2
            + self.base_starting_x,
            y=self.base_starting_y
            + (self.rows * self.cellH / 2)
            + 20
            + 2 * self.cellH,
            width=self.cellW / 2,
            height=self.rows * self.cellH / 2 - 20 - 2 * self.cellH,
        )

    def create_widgets(self, mode):
        self.fill_table_btn = Button(
            self,
            text=_("Fill table"),
            command=self.fill_table,
            bg=self.colors["main-bg"],
            fg="white",
            font=("Arial", 20, "bold"),
        )
        self.fill_table_btn.pack(side="left")

        if mode == "i":
            self.start_chat_btn = Button(
                self,
                text=_("Start game!"),
                command=self.start_chat,
                bg=self.colors["main-bg"],
                fg="white",
                font=("Arial", 20, "bold"),
            )
            self.start_chat_btn.pack(side="left")

            self.quit = Button(
                self,
                text=_("Close"),
                bg="red",
                fg="white",
                font=("Arial", 20, "bold"),
                command=self.master.destroy,
            )
            self.quit.pack(side="right")

            self.clear = Button(
                self,
                text=_("Clear"),
                command=self.clear_table,
                bg=self.colors["disabled-bg"],
                fg="white",
                font=("Arial", 20, "bold"),
            )
            self.clear.pack(side="right")
        elif mode == "t":
            self.start_chat_btn = Button(
                self,
                text=_("Start game!"),
                command=self.start_team_chat,
                bg=self.colors["main-bg"],
                fg="white",
                font=("Arial", 20, "bold"),
            )
            self.start_chat_btn.pack(side="left")

            self.quit = Button(
                self,
                text=_("Close"),
                bg="red",
                fg="white",
                font=("Arial", 20, "bold"),
                command=self.master.destroy,
            )
            self.quit.pack(side="right")

            self.clear = Button(
                self,
                text=_("Clear"),
                command=self.clear_team_table,
                bg=self.colors["disabled-bg"],
                fg="white",
                font=("Arial", 20, "bold"),
            )
            self.clear.pack(side="right")

    def fill_table(self):
        self.word_list_from_text()
        random.shuffle(self.players_colors)
        for i in range(self.rows):
            for j in range(self.columns):
                exec(
                    "self.e"
                    + str(i)
                    + str(j)
                    + ".config({'background': '"
                    + self.colors["main-bg"]
                    + "'})"
                )

                exec("self.e" + str(i) + str(j) + ".delete(0,END)")
                exec(
                    "self.e"
                    + str(i)
                    + str(j)
                    + ".insert(0, self.the_list[i][j])"
                )

    def word_list_from_text(self):
        raw_text = re.sub(r"[^a-zA-Z0-9]+", " ", text.raw)
        raw_text_list = raw_text.split(" ")
        entire_word_list = []
        [
            entire_word_list.append(x.lower())
            for x in raw_text_list
            if x.lower() not in entire_word_list and len(x) > 3
        ]

        random.shuffle(entire_word_list)
        word_list = entire_word_list[: self.columns * self.rows]
        formatted_word_list = []
        for i in range(self.rows):
            formatted_word_list.append(
                list(
                    word_list[
                        i * self.columns : i * self.columns + self.columns
                    ]
                )
            )

        self.the_list = formatted_word_list

    def start_chat(self):
        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((secret.server, secret.port))

        s.send(("PASS %s\r\n" % secret.oauth).encode("utf-8"))
        s.send(("NICK %s\r\n" % secret.username).encode("utf-8"))
        s.send(("JOIN #%s\r\n" % secret.channel).encode("utf-8"))
        allowed_players_list = self.get_allowed_players()
        self.send_message(
            _("Game has started, write the words in the chat!"), s
        )
        counter = 0
        total_counter = self.rows * self.columns
        game_active = True
        while game_active:
            raw_msg = s.recv(4096).decode("utf-8")
            print(raw_msg, "\n")
            # logging.info(raw_msg)
            messages = raw_msg.split("\r\n")

            for message in messages:
                if (
                    message.strip()
                    and "PRIVMSG #" + secret.username in message
                ):
                    username = re.search(r"\w+", message).group(0)
                    message = CHAT_MSG.sub("", message)
                    msg = message.replace("@", "")
                    logging.info("#########################")
                    logging.info("###Erabiltzailea: %s" % (username))
                    logging.info("   Originala: %s" % (raw_msg))
                    logging.info("   Aukeratua: %s" % (msg))
                    if allowed_players_list:
                        if username in allowed_players_list:
                            counter = counter + self.check_message(
                                username, msg
                            )
                    else:
                        counter = counter + self.check_message(username, msg)

                    if (
                        username == secret.username
                        and msg == "!stop"
                        or counter == total_counter
                    ):
                        game_active = False
                        self.send_message(_("Game Over!"), s)

    def start_team_chat(self):
        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((secret.server, secret.port))

        s.send(("PASS %s\r\n" % secret.oauth).encode("utf-8"))
        s.send(("NICK %s\r\n" % secret.username).encode("utf-8"))
        s.send(("JOIN #%s\r\n" % secret.channel).encode("utf-8"))
        self.taka_team = self.get_taka_team()
        self.tekla_team = self.get_tekla_team()
        self.send_message(
            _("Game has started, write the words in the chat!"), s
        )
        print(self.taka_team)
        counter = 0
        game_active = True
        self.players["taka"] = {"points": 0, "color": self.taka_color}
        self.players["tekla"] = {"points": 0, "color": self.tekla_color}
        while game_active:
            raw_msg = s.recv(4096).decode("utf-8")
            username = re.search(r"\w+", raw_msg).group(0)
            message = CHAT_MSG.sub("", raw_msg)
            if " PRIVMSG #" + secret.username + " :" in raw_msg:
                msg = message.replace("\r\n", "").replace("@", "")
                if username in self.taka_team:
                    counter = counter + self.check_team_message("taka", msg)
                elif username in self.tekla_team:
                    counter = counter + self.check_team_message("tekla", msg)

                if (
                    username == secret.username
                    and msg == "!stop"
                    or counter == (self.rows * self.columns)
                ):
                    game_active = False
                    self.send_message(_("Game Over!"), s)

    def check_team_message(self, team, msg):
        coor = self.search_text_match(msg)
        if coor:
            self.players[team]["points"] += len(msg)
            self.mark_as_done(coor, "@" + team)
            self.get_team_ranking()
            self.master.update()
            return 1
        return 0

    def check_message(self, username, msg):
        coor = self.search_text_match(msg)
        if coor:
            if not self.players.get(username):
                self.players[username] = {
                    "points": len(msg),
                    "color": self.players_colors[len(self.players.keys())],
                }
            else:
                self.players[username]["points"] += len(msg)
            self.mark_as_done(coor, "@" + username)
            self.get_ranking()
            self.master.update()
            return 1
        return 0

    def get_allowed_players(self):
        str_list = self.allowed_players.get("1.0", END).split("\n")
        return [i for i in str_list if i]

    def get_taka_team(self):
        str_list = self.taka.get("1.0", END).split("\n")
        return [i for i in str_list if i]

    def get_tekla_team(self):
        str_list = self.tekla.get("1.0", END).split("\n")
        return [i for i in str_list if i]

    def send_message(self, message, s):
        s.send(
            "PRIVMSG #{0} :{1}\r\n".format(secret.username, message).encode(
                "utf-8"
            )
        )

    def search_text_match(self, text):
        for i in range(self.rows):
            for j in range(self.columns):
                exec("self.to_search = self.e" + str(i) + str(j) + ".get()")
                if text.lower() == self.to_search.lower():
                    return [i, j]
        return False

    def mark_as_done(self, coor, username):
        i = coor[0]
        j = coor[1]
        player_color = self.players[username.replace("@", "")]["color"]
        exec(
            "self.e"
            + str(i)
            + str(j)
            + ".config({'background': '"
            + player_color
            + "'})"
        )
        exec("self.e" + str(i) + str(j) + ".delete(0,END)")
        exec("self.e" + str(i) + str(j) + ".insert(0, username)")

    def clear_table(self):
        for i in range(self.rows):
            for j in range(self.columns):
                exec(
                    "self.e"
                    + str(i)
                    + str(j)
                    + ".config({'background': '"
                    + self.colors["disabled-bg"]
                    + "'})"
                )
                exec("self.e" + str(i) + str(j) + ".delete(0,END)")
        self.players = {}
        self.winners.delete("1.0", END)

    def clear_team_table(self):
        for i in range(self.rows):
            for j in range(self.columns):
                exec(
                    "self.e"
                    + str(i)
                    + str(j)
                    + ".config({'background': '"
                    + self.colors["disabled-bg"]
                    + "'})"
                )
                exec("self.e" + str(i) + str(j) + ".delete(0,END)")
        self.players = {}
        self.taka_points.delete("1.0", END)
        self.tekla_points.delete("1.0", END)

    def get_ranking(self):
        ordered_players = ""
        for k, v in sorted(
            self.players.items(),
            key=lambda item: item[1]["points"],
            reverse=True,
        ):
            ordered_players += k + ": " + str(v["points"]) + "\n"
        self.winners.delete("1.0", END)
        self.winners.insert(END, ordered_players)

    def get_team_ranking(self):
        taka_points = self.players.get("taka").get("points")
        tekla_points = self.players.get("tekla").get("points")
        if taka_points > tekla_points:
            self.taka_points.config(font=("Arial", 50, "bold"))
            self.tekla_points.config(font=("Arial", 40))
        elif taka_points < tekla_points:
            self.tekla_points.config(font=("Arial", 50, "bold"))
            self.taka_points.config(font=("Arial", 40))
        else:
            self.tekla_points.config(font=("Arial", 45))
            self.taka_points.config(font=("Arial", 45))
        self.taka_points.delete("1.0", END)
        self.taka_points.insert(END, taka_points)
        self.tekla_points.delete("1.0", END)
        self.tekla_points.insert(END, tekla_points)
