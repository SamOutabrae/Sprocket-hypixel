import datetime, calendar, requests

def getUUID(username):
	"""
	Gets the UUID of a Minecraft user. If the username is already a UUID, it returns the UUID.
	"""

	if(len(username) == 32):
		return username

	try:
		d = datetime.datetime.now()
		timestamp = calendar.timegm(d.utctimetuple())

		url = "https://api.mojang.com/users/profiles/minecraft/{0}?at={1}".format(username, timestamp)
		data = requests.get(url).json()
		return data["id"]
	except:
		return None

prestiges = [
        ("Rookie", 50),
        ("Rookie 2", 60),
        ("Rookie 3", 70),
        ("Rookie 4", 80),
        ("Rookie 5", 90),
        ("Iron", 100),
        ("Iron 2", 130),
        ("Iron 3", 160),
        ("Iron 4", 190),
        ("Iron 5", 220),
        ("Gold", 250),
        ("Gold 2", 300),
        ("Gold 3", 350),
        ("Gold 4", 400),
        ("Gold 5", 450),
        ("Diamond", 500),
        ("Diamond 2", 600),
        ("Diamond 3", 700),
        ("Diamond 4", 800),
        ("Diamond 5", 900),
        ("Master", 1000),
        ("Master 2", 1200),
        ("Master 3", 1400),
        ("Master 4", 1600),
        ("Master 5", 1800),
        ("Legend", 2000),
        ("Legend 2", 2600),
        ("Legend 3", 3200),
        ("Legend 4", 3800),
        ("Legend 5", 4400),
        ("Grandmaster", 5000),
        ("Grandmaster 2", 6000),
        ("Grandmaster 3", 7000),
        ("Grandmaster 4", 8000),
        ("Grandmaster 5", 9000),
        ("Godlike", 10000),
        ("Godlike 2", 12000),
        ("Godlike 3", 14000),
        ("Godlike 4", 16000),
        ("Godlike 5", 18000),
        ("Godlike 6", 20000),
        ("Godlike 7", 22000),
        ("Godlike 8", 24000),
        ("Godlike 9", 26000),
        ("Godlike 10", 28000)
    ]

def winsToPrestige(wins):
	for idx, prestige in enumerate(prestiges):
		winsNeeded = prestige[1]
		prestige = prestige[0]

		if winsNeeded > wins:
			return (prestige, winsNeeded-wins)

def getPrestige(wins):
	last = "N/A"

	for prestige, winsNeeded in prestiges:
		if wins < winsNeeded:
			break

			last = prestige

	return last

