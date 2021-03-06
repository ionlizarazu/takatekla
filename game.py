from tkinter import *
import random
import text

import socket
import secret

import re


class Game(Frame):

    def __init__(self, cellW, cellH, rows, columns, master, colors={"main-bg": "#146791", "disabled-bg": "#7798a8"}):
        super().__init__(master)
        master.configure(background='white')
        master.title("TAKATEKLA")
        master.geometry(str(columns * cellW + 30 + cellW +
                            30) + 'x' + str((rows * cellH) + 80))
        self.master = master
        self.cellW = cellW
        self.cellH = cellH
        self.rows = rows
        self.columns = columns
        self.colors = colors
        self.to_search = ''
        self.the_list = []
        self.players = {}
        self.players_colors = ['deep sky blue', 'dark turquoise', 'medium aquamarine', 'dark green', 'sea green', 'goldenrod', 'indian red',
                               'dark orange', 'orange red', 'violet red', 'dark violet', 'blue4', 'SeaGreen3', 'OliveDrab4', 'IndianRed4', 'tomato3']
        self.init_table()
        self.pack()
        self.create_widgets()

    def init_table(self):
        # table_starting_point = 15 + self.cellW
        for i in range(self.rows):
            for j in range(self.columns):
                exec("self.e" + str(i) + str(j) +
                     " = Entry(self.master, bg='" + self.colors["disabled-bg"] + "', fg='white', font=('Arial', 22, 'bold'), justify=CENTER)")
                exec("self.e" + str(i) + str(j) + ".grid(row=i, column=j)")
                exec("self.e" + str(i) + str(j) +
                     ".place(x=j*self.cellW + 15, y=i*self.cellH+70, height=self.cellH, width=self.cellW)")
                exec("self.e" + str(i) + str(j) + ".insert(END, '')")

        self.allowed_players_label = Label(
            self.master, text="Allowed players:")
        self.allowed_players_label.place(x=15 + self.columns * self.cellW + 15,
                                         y=70, width=self.cellW)

        self.allowed_players = Text(self.master)
        self.allowed_players.place(x=15 + self.columns * self.cellW + 15,
                                   y=70 + 20, width=self.cellW, height=self.rows * self.cellH / 2 - 20)

        self.winners_label = Label(self.master, text="Ranking:")
        self.winners_label.place(x=15 + self.columns * self.cellW + 15,
                                 y=70 + (self.rows * self.cellH / 2), width=self.cellW)

        self.winners = Text(self.master)
        self.winners.place(x=15 + self.columns * self.cellW + 15,
                           y=70 + (self.rows * self.cellH / 2) + 20, width=self.cellW, height=self.rows * self.cellH / 2 - 20)

    def create_widgets(self):
        self.fill_table_btn = Button(self, text="Fill table", command=self.fill_table,
                                     bg=self.colors["main-bg"], fg="white", font=('Arial', 20, 'bold'))
        self.fill_table_btn.pack(side="left")

        self.start_chat_btn = Button(self, text="Start game!", command=self.start_chat,
                                     bg=self.colors["main-bg"], fg="white", font=('Arial', 20, 'bold'))
        self.start_chat_btn.pack(side="left")

        self.quit = Button(self, text="Close", bg="red", fg="white", font=('Arial', 20, 'bold'),
                           command=self.master.destroy)
        self.quit.pack(side="right")

        self.clear = Button(self, text="Clear", command=self.clear_table,
                            bg=self.colors["disabled-bg"], fg="white", font=('Arial', 20, 'bold'))
        self.clear.pack(side="right")

    def fill_table(self):
        self.word_list_from_text()
        random.shuffle(self.players_colors)
        for i in range(self.rows):
            for j in range(self.columns):
                exec("self.e" + str(i) + str(j) +
                     ".config({'background': '" + self.colors["main-bg"] + "'})")

                exec("self.e" + str(i) + str(j) + ".delete(0,END)")
                exec("self.e" + str(i) + str(j) +
                     ".insert(0, self.the_list[i][j])")

    def word_list_from_text(self):
        raw_text = re.sub(r"[^a-zA-Z0-9]+", ' ', text.raw)
        raw_text_list = raw_text.split(' ')
        entire_word_list = []
        [entire_word_list.append(
            x.lower()) for x in raw_text_list if x not in entire_word_list and len(x) > 3]

        random.shuffle(entire_word_list)
        word_list = entire_word_list[:self.columns * self.rows]
        formatted_word_list = []
        for i in range(self.rows):
            formatted_word_list.append(
                list(word_list[i * self.columns:i * self.columns + self.columns]))

        self.the_list = formatted_word_list

    def start_chat(self):
        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((secret.server, secret.port))

        s.send(('PASS %s\r\n' % secret.oauth).encode('utf-8'))
        s.send(('NICK %s\r\n' % secret.username).encode('utf-8'))
        s.send(('JOIN #%s\r\n' % secret.channel).encode('utf-8'))
        allowed_players_list = self.get_allowed_players()
        self.send_message("Game has started, write the words in the chat!", s)
        counter = 0
        game_active = True
        while game_active:
            raw_msg = s.recv(4096).decode('utf-8')
            username = re.search(r"\w+", raw_msg).group(0)
            message = CHAT_MSG.sub("", raw_msg)
            if ' PRIVMSG #' + secret.username + ' :' in raw_msg:
                msg = message.replace('\r\n', '').replace('@', '')
                if allowed_players_list:
                    if username in allowed_players_list:
                        counter = counter + self.check_message(username, msg)
                else:
                    counter = counter + self.check_message(username, msg)

                if username == secret.username and msg == '!g' or counter == (self.rows * self.columns):
                    game_active = False
                    self.send_message("Game Over!", s)

    def check_message(self, username, msg):
        coor = self.search_text_match(msg)
        if coor:
            if not self.players.get(username):
                self.players[username] = {"points": len(msg), "color": self.players_colors[
                    len(self.players.keys())]}
            else:
                self.players[username]["points"] += len(msg)
            self.mark_as_done(coor, '@' + username)
            self.get_ranking()
            self.master.update()
            return 1
        return 0

    def get_allowed_players(self):
        str_list = self.allowed_players.get('1.0', END).split('\n')
        return [i for i in str_list if i]

    def send_message(self, message, s):
        s.send("PRIVMSG #{0} :{1}\r\n".format(
            secret.username, message).encode('utf-8'))

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
        player_color = self.players[username.replace('@', '')]['color']
        exec("self.e" + str(i) + str(j) +
             ".config({'background': '" + player_color + "'})")
        exec("self.e" + str(i) + str(j) + ".delete(0,END)")
        exec("self.e" + str(i) + str(j) + ".insert(0, username)")

    def clear_table(self):
        for i in range(self.rows):
            for j in range(self.columns):
                exec("self.e" + str(i) + str(j) +
                     ".config({'background': '" + self.colors["disabled-bg"] + "'})")
                exec("self.e" + str(i) + str(j) + ".delete(0,END)")
        self.players = {}
        self.winners.delete('1.0', END)

    def get_ranking(self):
        ordered_players = ""
        for k, v in sorted(self.players.items(), key=lambda item: item[1]['points'], reverse=True):
            ordered_players += k + ": " + str(v['points']) + "\n"
        self.winners.delete('1.0', END)
        self.winners.insert(END, ordered_players)
