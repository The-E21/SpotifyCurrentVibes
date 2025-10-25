# SpotifyCurrentVibes

A simple python console project to help manage a spotify playlist called **Current Vibes** containing songs you are enjoying the vibe of currently and want to hear more of for the time being.

The project contains functions to add songs to the playlist and also to remove songs that have existed in the playlist for longer than a choosen amount of time (two weeks by default)

The project also adds songs added to Current Vibes to a montly playlist, that the songs will never be removed from (unless you remove them manually), as a reminder of what songs you added to Current Vibes that month.

Current Vibes is created automatically the first time you run the project and monthly playlists are automatically created the first time you run the program in a new month

### Install guide

- You will need python installed to run the program, the project has been tested on python 3.10.12

- Clone the repository: `git clone https://github.com/The-E21/SpotifyCurrentVibes`

- Go to the [spotify's developer website](https://developer.spotify.com) and [create an app](https://developer.spotify.com/documentation/web-api/concepts/apps), you will need to give the app a redirect uri, a random port on 127.0.0.1 works

- If you wish create a new virtual enviroment

- Install the required packages using `pip install -r requirements.txt`

- Run the program using `python main.py`

- The first time you run the project, you will need to enter the client id, client secret and redirect uri of the spotify app you created

### How to use

Run the program with `python main.py`

The program prompts you on what functions you want to call to manage the playlist until you exit the program

The options are as follows:

1. Removes songs on current vibes that have been on the playlist for longer than the allowed time

2. Add a song to current vibes and the monthly playlist, after selecting this option you will need to paste the song share link into the terminal. This can be found on spotify by clicking the three dots next to the song, share and copy link.

3. Add a song to current vibes from your last 10 listened to songs. Instead of entering the songs share link, the 10 songs you last played will be listed and you must enter a number from 1-10 corrisponding to the song you want to add

4. Changes the amount of time songs are allowed to exist on current vibes for. (If you reduced the time, you may want to use function 1 to remove old songs that would have remained before the change)

5. Exits the program