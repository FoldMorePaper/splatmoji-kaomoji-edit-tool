from hashlib import sha256

DB_FILE = "kaomoji.txt"

class KaomojiDB:
    """Offers facilities to edit and check the DB file."""

    kaomojis = list()

    def __init__(self, filename=False):

        if filename:
            self.load(filename=filename)

    def load(self, filename):
        """Loads a db file."""

        with open(filename) as dbfile:
            lines = dbfile.readlines()

        for line in lines:

            code, keywords = line.strip().split("\t")

            kaomoji = Kaomoji(code=code, keywords=keywords)

            # TODO: FIXME: WE NEED TO CHECK IF KAOMOJI EXISTS TO UPDATE INSTEAD
            #  OF ADDING, HERE:
            self.kaomojis.append(kaomoji)

    def write(self):
        """Writes a db file."""
        pass

    def entity_exists(self, kaomoji: Kaomoji):
        """Checks if a kaomoji exists already in the database."""
        pass

    def update_entity(self, kaomoji: Kaomoji):
        """Updates keywords to database."""
        pass

class Kaomoji:
    """Represents an Kaomoji entity."""

    code = str()  # unicode of the kaomoji
    keywords = list()  # list of strings

    def __init__(self, code, keywords=False):

        self.code = code

        if keywords:
            self.keywords = keywords.split(',')

        self.hash = self._makehash(code)

    def add_keywork(self, keyword):
        self.keywords.append(keyword)

    def _makehash(self, code):
        """Gives a UUID for a given kaomoji, for comparison.

        It is the base10 of the sha256 digest of the kaomoji code:
            HASH = INT10(SHA256(KAOMOJI_CODE))

        With this we can know if some emoji is already on the DATABASE, so to
            append keywords to it.
        """

        code_bytes = code.encode("utf-8")
        code_sha256_hex_digestion = sha256(code_bytes).hexdigest()

        the_hash = int(code_sha256_hex_digestion, base=16)

        return the_hash

    def __hash__(self):
        return self.hash

    def __repr__(self):
        return "<Kaomoji `{}'>".format(self.code)

    def __str__(self):
        return self.code


db = KaomojiDB(file=DB_FILE)

code = input("code pls?: ")

new_kaomoji = Kaomoji(code)
print(new_kaomoji)
print(new_kaomoji.hash)

while True:
    keyword = input("Type new keyword (CTRL-c to END): ")
    new_kaomoji.add_keywork(keyword)