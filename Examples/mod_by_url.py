from pprint import pprint as print

from nexuswrapper.nexus import Nexus

nexus = Nexus()
mod = nexus.mod_by_url("https://www.nexusmods.com/fallout76/mods/84")
print(mod)


