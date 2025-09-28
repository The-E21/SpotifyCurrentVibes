from backend import backend
import authenticator

# Try to login, if can great, if not prompt user to enter auth details

auth_data = {}

try:
    auth_data = authenticator.read_auth_data()
except FileNotFoundError:
    while True:
        print("No auth data found")
        print("Enter client id:")
        auth_data["client_id"] = input()
        print("Enter client secret")
        auth_data["client_secret"] = input()
        print("Enter redirect uri")
        auth_data["redirect_uri"] = input()

        print("Client id:", auth_data["client_id"])
        print("Client secret:", auth_data["client_secret"])
        print("Redirect uri:", auth_data["redirect_uri"])

        print("\nIs the above correct? (y/n)")
        answer = input()
        if answer.lower() == "y":
            authenticator.write_auth_data(auth_data["client_id"], auth_data["client_secret"], auth_data["redirect_uri"])
            break

be = backend(auth_data["client_id"], auth_data["client_secret"], auth_data["redirect_uri"])

# Ask user what needs happening

options = ["Remove old songs from playlist", 
           "Add a new song to the playlist using it's id or song link",
           "Add a recently played song to the playlist",
           "Change the amount of time songs stay on playlist for",
           "Exit"]

# 1 - Remove old songs
def refresh_playlist():
    be.refresh()
    print("Playlist updated")

# 2 - Add a song using an id
def add_song_id():
    print("Please enter the song id or share link:")
    id = input()
    try:
        be.add_song(id)
        print("Song added to playlist")
    except:
        print("Error, cannot find the given song")

# 3 - Add recently listened to song
def add_song_recent():
    DISPLAY_NUM = 10

    print("Which song would you like to add? (0-%d)\n"%DISPLAY_NUM)
    recent_songs = be.get_recently_listened_to(DISPLAY_NUM - 1)
    for idx, song in enumerate(recent_songs):
        print("%d:"%(idx+1), song["artists"][0]["name"], " – ", song["name"])
    print("0: Cancel")

    while True:
        answer = input()
        if answer == "q" or answer == "Q" or answer == "0":
            print("No new song added")
            return

        try:
            answer = int(answer) - 1
            be.add_song(recent_songs[answer]["id"])
            print(recent_songs[answer]["name"], "added to playlist")
            return
        
        except:
            print("Please enter a number from (0-%d)"%DISPLAY_NUM)

# 4 - Change time a song is allowed on the playlist
def change_refresh_time():
    while True:
        print("How many days should songs stay on the playlist for? (enter \"q\" to cancel)")
        answer = input()
        if answer.lower() == "q":
            print("Canceled")
            return
        
        try:
            answer = float(answer)
            assert answer > 0
            be.set_wait_time(86400 * answer)
            print("Changed wait time")
            return
        
        except:
            print("Please enter a possitive number")

# 5 - quit
def exit_program():
    print("Quitting program...")
    quit()

while True:
    print("Please select an option: (1-%d)\n"%len(options))
    for i, option in enumerate(options):
        print("%d:"%(i+1), option)
    
    answer = input()
    match answer:
        case "1":
            refresh_playlist()
        case "2":
            add_song_id()
        case "3":
            add_song_recent()
        case "4":
            change_refresh_time()
        case "5" | "q" | "Q":
            exit_program()
        case _:
            print("Please enter a number from 1-%d"%len(options))
    
    print("\n")