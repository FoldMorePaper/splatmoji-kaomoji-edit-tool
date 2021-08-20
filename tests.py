from kaomoji import KaomojiDB
from kaomoji import Kaomoji

DB_FILE = "kaomoji.txt"

#db = KaomojiDB(filename=DB_FILE)

code = input("code pls?: ")

new_kaomoji = Kaomoji(code)
print(new_kaomoji)
print(new_kaomoji.hash)

while True:
    keyword = input("Type new keyword (enter /end to end): ")
    if keyword == "/end":
        break
    new_kaomoji.add_keywork(keyword)
