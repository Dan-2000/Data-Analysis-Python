import requests
base_url = "https://itunes.apple.com/search?"
r = requests.get(base_url, params = {"term": "metallica", "country": "us", "limit": "200"})
data = r.json()
song_release_date= []
for track in data["results"]:
        track_name=track.get("trackName")
        release_Date=track.get("releaseDate")
        song_release_date.append({"trackName": track_name, "releaseDate": release_Date})
user_date = input("Please enter the year you would like to check Metalica releases(YYYY):")
for song in song_release_date:
    release_year =song["releaseDate"][:4]
    if(release_year == user_date):
                print("Track Name:{0} \nRelease Date:{1} \n".format(song["trackName"],song["releaseDate"]))