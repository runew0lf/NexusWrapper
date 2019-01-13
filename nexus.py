import asyncio
import hashlib
import json
import time
import uuid
import webbrowser
from pprint import pprint as print

import requests
import websockets
from clint.textui import progress


class Nexus():
    def __init__(self):
        self.session = requests.Session()
        self.api_key = ""
        self.BASE_URL = "https://api.nexusmods.com/v1/"
        try:
            with open('nexus.json', 'r') as fh:
                nexus_data = json.load(fh)
                self.api_key = nexus_data.get('api_key')
        except FileNotFoundError:
            self.api_key = asyncio.get_event_loop().run_until_complete(self.get_api_key())
            with open('nexus.json', 'w') as fh:
                json.dump({"api_key": self.api_key}, fh, indent=4)

        self.headers = {"content-type": "application/json", "APIKEY": self.api_key}

    async def get_api_key(self):
        async with websockets.connect('wss://sso.nexusmods.com') as websocket:
            id = str(uuid.uuid4())
            await websocket.send(json.dumps({'id': id, 'appid': 'Vortex'}))
            webbrowser.open(f"https://www.nexusmods.com/sso?id={id}")
            api_key = await websocket.recv()
            return api_key

    def request_data(self, endpoint):
        time.sleep(1)  # limit to 1 request per second
        r = self.session.request('GET', self.BASE_URL + endpoint, headers=self.headers, timeout=30)
        return r.json()

    def validate(self):
        return self.request_data("users/validate.json")

    def games(self):
        return self.request_data("games")

    def game(self, game_name):
        self.game_name = game_name
        return self.request_data(f"games/{game_name}")

    def mod(self, game_name, mod_id):
        return self.request_data(f"games/{game_name}/mods/{mod_id}")

    def file_list(self, game_name, mod_id):
        return self.request_data(f"games/{game_name}/mods/{mod_id}/files")

    def file_info(self, game_name, mod_id, file_id):
        return self.request_data(f"games/{game_name}/mods/{mod_id}/files/{file_id}")

    def download_link(self, game_name, mod_id, file_id):
        return self.request_data(f"games/{game_name}/mods/{mod_id}/files/{file_id}/download_link")

    def get_file_by_md5(self, game_name, md5):
        return self.request_data(f"games/{game_name}/mods/md5_search/{md5}")

    def calc_md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def mod_by_url(self, url):
        url = url.split('?', 1)[0]
        game = url.split("/")[3]
        mod_id = url.split(f"/{game}/mods/", 1)[1]
        mod_id = mod_id.replace("/", "")
        return self.request_data(f"games/{game}/mods/{mod_id}")

    def download_file(self, file_id, fname):
        r = requests.get(file_id, stream=True)
        with open(fname, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def search(self, search_term, game_id=None):
        URL = f"https://search.nexusmods.com/mods?terms={search_term}&game_id={game_id}".replace(" ", ",")
        time.sleep(1)  # limit to 1 request per second
        r = self.session.request('GET', URL, timeout=30)
        return r.json()

