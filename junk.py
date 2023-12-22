import qrcode
with open("junk.txt", "r") as f:
    data = f.read()
with open("testcase-write.txt", "w") as f:
    f.write("WELCOME TO THE SPOTIFY YYYY_MM_DD PLAYLIST")
    f.write(data)
with open("testcase-write.txt", "r") as f:
    rec = f.read()

img = qrcode.make(rec)
img.save('test_qr.png')
