from spotify_connect import song_urls, ask
import qrcode
import pymongo
import gridfs

with open("songs.txt", "w") as f:
    f.write(f"WELCOME TO THE SPOTIFY {ask} PLAYLIST\n")
    for key, val in song_urls.items():
        f.write('%s : %s\n' % (key, val))

with open("songs.txt", "r") as f:
    data = f.read()

img = qrcode.make(data)
img.save('songs_qr.jpg')

client = pymongo.MongoClient(
    "mongodb+srv://anandprajwal123:praj123@top-songs-on-given-date.deehg5b.mongodb.net/?retryWrites=true&w=majority")

db = client["Data"]
collections = db["Details"]

fs = gridfs.GridFS(db)
file = "songs_qr.jpg"
with open(file, 'rb') as f:
    contents = f.read()
fid = fs.put(contents, filename='file')

rec = {
    "Filename": f"Top Songs of {ask}",
    "Top Songs": fid
}
collections.insert_one(rec)
