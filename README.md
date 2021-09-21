# Takatekla
Takatekla is a Twitch based game, where the people in the chat are the gamer and the streamer spectator.

## How to use
First of all, is required the Tkinter Python interface to Tcl/Tk. You will have no problem if you are using Python3.8.
Afer warnings, clone this repository
```
$ git clone git@github.com:ionlizarazu/takatekla.git
```

### Configure it for your stream
You have to create the secret.py file, and fill the username, oauth and channel parameters.
```
# you don't need to replace server and port
server = "irc.chat.twitch.tv"
port = 6667
# the username you are going to use to send messages
username = 'username'
# the oauth code to connect with your user
# get it at https://twitchapps.com/tmi/
oauth = "oauth:2432hjk342bn54jkbhjk543jhk543b"
# the channel name you are goingo to connect to
channel = 'channelname'
```
To get your oauth visit https://twitchapps.com/tmi/

### Some extra configuration
You can configure your language preferences at config.py file.

### Color configuration
If you don't like default colors, you can modify the main and disabled colors at chat.py

### Select the text to get the words
You can modify the text.py raw parameter to get your own words list. You have to copy any newspaper text and paste it on a single line. The app cleans and builds the array to use it.

### Start the application
You can create your custom table size, starting from 1x1 to anything you want.
```
$ cd takatekla
$ python3 takatekla.py 4 4
```
![irudia](https://user-images.githubusercontent.com/5443301/110205524-b3a45a00-7e78-11eb-96d7-80c011881455.png)

Once you have started the application, you can allow to play anyone in the chat (geting empty the allowed players field) or only allow some selected people writing their username (one per line) in the text box.

When you are ready to start the game, you can "Fill table" and then "Start game!". At this time the game connects with your stream and sends a message saying "Game has started, write the words in the chat!".

Now people have write the words at the screen to get points and win the game. Here is my stream exaple:
![irudia](https://user-images.githubusercontent.com/5443301/110205693-e4d15a00-7e79-11eb-9274-983440d7f1de.png)

As you can see, the "Ranking" text box is updated every word match, and offers you a chance

## Add translations

### Get new texts from code
Most of translations are at game.py, so you can execute:
```
$ pygettext3 -d base -o locales/base.pot game.py
```
This way you can get the new translation needed texts.

### Merge base pot file with each language
```
$ msgmerge --update locales/eu/LC_MESSAGES/base.po locales/base.pot
$ msgmerge --update locales/en/LC_MESSAGES/base.po locales/base.pot
```

### Compile po files
After translating them, compile the po files for each langauage.
```
$ msgfmt -o locales/eu/LC_MESSAGES/base.mo locales/eu/LC_MESSAGES/base
$ msgfmt -o locales/en/LC_MESSAGES/base.mo locales/en/LC_MESSAGES/base
```
