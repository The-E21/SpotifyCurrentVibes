import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

class backend:
    def __init__(self):
        scope = ["playlist-modify-private", "user-read-recently-played", "user-read-playback-state"]
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        
        self.DATA_FILE_NAME = "data.json"
        try:
            with open(self.DATA_FILE_NAME, "r") as file:
                self.data = json.load(file)
        except:
            self.first_time_setup()
        
    
    def first_time_setup(self):
        DEFAULT_PLAYLIST_NAME = "Current Vibes"
        DEFAULT_WAIT_TIME = 1209600

        sp_user = self.sp.current_user()
        user_name = sp_user['uri'].split(":")[2]
        playlist = self.sp.user_playlist_create(user_name,DEFAULT_PLAYLIST_NAME, public=False)

        self.data = {"playlist_id" : playlist["id"], "wait_time" : DEFAULT_WAIT_TIME}
        self.write_data_to_file()

    def get_playlist_items(self):
        return self.sp.playlist_items(self.data["playlist_id"])
    
    def get_recently_listened_to(self):
        rtn = []

        current = self.sp.current_user_playing_track()
        recent = self.sp.current_user_recently_played()

        if current != None and current["item"]["id"] != recent["items"][0]["track"]["id"]:
            rtn.append(current["item"])

        for item in recent["items"]:
            rtn.append(item["track"])

        return rtn

    def add_song(self, id):
        self.sp.playlist_add_items(self.data["playlist_id"], [id])

    def refresh(self):
        pass

    def set_wait_time(self, time):
        self.data["wait_time"] = time
        self.write_data_to_file()
    
    def write_data_to_file(self):
        json_str = json.dumps(self.data, indent=4)
        with open(self.DATA_FILE_NAME, "w") as file:
            file.write(json_str)
