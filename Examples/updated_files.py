from pprint import pprint as print

from nexuswrapper.nexus import Nexus

nexus = Nexus()
mods = nexus.updated_files("fallout4")
print(mods)