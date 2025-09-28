import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime, timezone, timedelta

class backend:
    def __init__(self):
        scope = ["playlist-modify-private", "user-read-recently-played", "user-read-playback-state"]
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        
        self.DATA_FILE_NAME = "data.json"
        try:
            with open(self.DATA_FILE_NAME, "r") as file:
                self.data = json.load(file)
            
            self.check_for_new_month()

        except:
            self.first_time_setup()
        
    
    def first_time_setup(self):
        DEFAULT_PLAYLIST_NAME = "Current Vibes"
        DEFAULT_WAIT_TIME = 1209600

        playlist = self.create_playlist(DEFAULT_PLAYLIST_NAME)

        self.data = {"playlist_id" : playlist["id"], "wait_time" : DEFAULT_WAIT_TIME}
        self.start_new_month(datetime.now())

    def create_playlist(self, playlist_name) -> dict:
        sp_user = self.sp.current_user()
        user_name = sp_user['uri'].split(":")[2]
        return self.sp.user_playlist_create(user_name,playlist_name, public=False)

    def get_playlist_items(self) -> dict:
        return self.sp.playlist_items(self.data["playlist_id"])["items"]
    
    def get_recently_listened_to(self) -> dict:
        rtn = []

        current = self.sp.current_user_playing_track()
        recent = self.sp.current_user_recently_played()

        if current != None and current["item"]["id"] != recent["items"][0]["track"]["id"]:
            rtn.append(current["item"])

        for item in recent["items"]:
            rtn.append(item["track"])

        return rtn

    def add_song(self, id):
        self.check_for_new_month()
        self.sp.playlist_add_items(self.data["playlist_id"], [id])

        month_tracks = self.sp.playlist_items(self.data["month_playlist_id"])["items"]
        for item in month_tracks:
            if item["track"]["id"] == id:
                return

        self.sp.playlist_add_items(self.data["month_playlist_id"], [id])

    def refresh(self):
        results = self.get_playlist_items()
        to_remove = []
        for item in results:
            if self.query_remove_item(item):
                to_remove.append(item["track"]["id"])
        
        if len(to_remove) > 0:
            self.sp.playlist_remove_all_occurrences_of_items(self.data["playlist_id"], to_remove)
    
    def query_remove_item(self, item) -> bool:
        added = datetime.strptime(item["added_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        time_since_added = datetime.now(timezone.utc) - added
        return time_since_added > timedelta(seconds=self.data["wait_time"])

    def set_wait_time(self, time):
        self.data["wait_time"] = time
        self.write_data_to_file()
    
    def write_data_to_file(self):
        json_str = json.dumps(self.data, indent=4)
        with open(self.DATA_FILE_NAME, "w") as file:
            file.write(json_str)
    
    def check_for_new_month(self):
        current_date = datetime.now()
        if self.data["current_month"] != current_date.month:
            self.start_new_month(current_date)

    def start_new_month(self, current_date):
        self.data["current_month"] = current_date.month
        month_playlist = self.create_playlist(current_date.strftime("%B %y"))
        self.data["month_playlist_id"] = month_playlist["id"]
        self.write_data_to_file()
