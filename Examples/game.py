from pprint import pprint as print

from nexuswrapper.nexus import Nexus

nexus = Nexus()
game = nexus.game("Fallout76")
print(game)
