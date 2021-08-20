from kaomoji import KaomojiDB
from kaomoji import Kaomoji

#DB_FILE = "kaomoji.txt"
DB_FILE = "emoticons.tsv"

#db = KaomojiDB(filename=DB_FILE)
db = KaomojiDB()
db.load_file(filename=DB_FILE)

print(db.entry_num, "kaomojis loaded")

code = input("code pls?: ")

new_kaomoji = Kaomoji(code)

if db.kaomoji_exists(new_kaomoji):
    print("Already on the database")
    # return the kaomoji with the keywords if it has some
    new_kaomoji = db.get_kaomoji_by_kaomoji(new_kaomoji)
    print("The kaomoji already exists with the keywords: ",
          ",".join(new_kaomoji.keywords))
else:
    print("Not on the database yet.")

while True:

    keyword = input("Type new keyword (enter /end to end): ")

    if keyword == "/end":
        break

    new_kaomoji.add_keywork(keyword)

db.update_kaomoji(kaomoji=new_kaomoji)
db.write()