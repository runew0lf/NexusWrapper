from pprint import pprint as print

from nexuswrapper.nexus import Nexus

nexus = Nexus()
games = nexus.games()
for game in games:
    name = game['name']
    if name == "Mafia III":
        print(game)

print(f"There are {len(games)} games on nexus right now.")
