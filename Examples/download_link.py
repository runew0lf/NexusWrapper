from pprint import pprint as print

from nexuswrapper.nexus import Nexus

nexus = Nexus()
uri = nexus.download_link("Fallout76", "84", "378")
print(uri)

nexus.download_file(uri[0]['URI'], 'Examples\\glow-loose-84-1-5-1543597528.7z')