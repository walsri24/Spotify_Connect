import gridfs
import pymongo
from PIL import Image
import os
import io


def read_image(path):
    count = os.stat(path).st_size / 2
    with open(path, "rb") as fi:
        return bytearray(fi.read())


client = pymongo.MongoClient(
    "mongodb+srv://anandprajwal123:praj123@top-songs-on-given-date.deehg5b.mongodb.net/?retryWrites=true&w=majority")

db = client["Data"]
collections = db["Details"]

fs = gridfs.GridFS(db)

with open("songs_qr.jpg", "rb") as f:
    content = f.read()
    # print(f.tell())

fid = fs.put(content, filename='file')

# print(fs.exists(fid))

data = fs.get(fid).read()
# print(data)
with open("Byte_Array_of_Image.txt", "wb") as f:
    f.write(data)

bytes_ = read_image("Byte_Array_of_Image.txt")
image = Image.open(io.BytesIO(bytes_))
# print(image)
image.save('decoded.jpg')
