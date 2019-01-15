from pprint import pprint as print

from nexuswrapper.nexus import Nexus

nexus = Nexus()
mod = nexus.file_info("Fallout76", "84", "378")
print(mod)