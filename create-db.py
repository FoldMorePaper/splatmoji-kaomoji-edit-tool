DB_FILE = "kaomoji.txt"

class Kaomoji:

    code = str()  # unicode of the kaomoji
    keywords = list()  # list of strings

    def __init__(self, code):

        self.code = code

    def add_keywork(self, keyword):
        self.keywords.append(keyword)

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<Kaomoji `{}'>".format(self.code)

code = input("code pls? ")

new_kaomoji = Kaomoji(code)
print(new_kaomoji)
