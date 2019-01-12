import requests
import websockets
import webbrowser
import asyncio
import uuid
import json
from pprint import pprint as print


class Nexus():
    def __init__(self):
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

    async def get_api_key(self):
        async with websockets.connect('wss://sso.nexusmods.com') as websocket:
            id = str(uuid.uuid4())
            await websocket.send(json.dumps({'id': id, 'appid': 'Vortex'}))
            webbrowser.open(f"https://www.nexusmods.com/sso?id={id}")
            api_key = await websocket.recv()
            return api_key

    def request_data(self, endpoint):
        headers = {"content-type": "application/json", "APIKEY": self.api_key}
        r = requests.get(f"{self.BASE_URL}{endpoint}", headers=headers)
        return(r.json())

    def validate(self):
        return self.request_data("users/validate.json")

    def games(self):
        return self.request_data("games")

    def game(self, game_name):
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

nexus = Nexus()
print(nexus.test())
