from pprint import pprint as print

from nexuswrapper.nexus import Nexus

nexus = Nexus()
mod = nexus.search("Recipes and Plans Glow")
print(mod)