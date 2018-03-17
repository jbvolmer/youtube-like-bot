#infinite chill / 2018
all: clean youtube-like-bot run

youtube-like-bot: youtube-like-bot.py
	cp youtube-like-bot.py youtube-like-bot
	chmod u+x youtube-like-bot
run:
	./youtube-like-bot


clean:
	rm -f youtube-like-bot
