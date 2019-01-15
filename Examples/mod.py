from pprint import pprint as print

from nexuswrapper.nexus import Nexus

nexus = Nexus()
mod = nexus.mod("Fallout76", "84")
print(mod)
