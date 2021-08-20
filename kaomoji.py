from hashlib import sha256

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


    def __eq__(self, other):
        return hash(self) == hash(other)


    def __hash__(self):
        return self.hash


    def __repr__(self):
        return "<Kaomoji `{}'; kwords: `{}'>".format(self.code, self.keywords)


    def __str__(self):
        return self.code


class KaomojiDB:
    """Offers facilities to edit and check the DB file."""

    #db_file = None
    filename = str()
    kaomojis = list()
    entry_num = int()


    def __init__(self, filename=None):

        if filename:

            self.filename = filename
            self.load_file(filename=filename)


    def load_file(self, filename):
        """Loads a db file."""

        self.db_file = open(filename)
        #with open(filename) as dbfile:
        lines = db_file.readlines()

        for line in lines:

            code, keywords = line.strip().split("\t")

            kaomoji = Kaomoji(code=code, keywords=keywords)

            # TODO: FIXME: WE NEED TO CHECK IF KAOMOJI EXISTS TO UPDATE INSTEAD
            #  OF ADDING, HERE:
            self.kaomojis.append(kaomoji)


    def write(self):
        """Writes a db file."""

        for kaomoji in self.kaomojis:
            code = kaomoji.code
            keywords_string = ",".join(kaomoji.keywords)
            db_line = "{0}\t{1}\n".format(code, keywords_string)


    def kaomoji_exists(self, kaomoji: Kaomoji):
        """Checks if a kaomoji exists already in the database."""
        pass


    def add_kaomoji(self, kaomoji: Kaomoji):
        """Adds a Kaomoji to the database."""
        pass


    def remove_kaomoji(self, kaomoji: Kaomoji):
        """Removes a Kaomoji from the database."""
        pass


    def update_kaomoji(self, kaomoji: Kaomoji):
        """Updates keywords to database."""
        pass




# db = KaomojiDB(file=DB_FILE)
#
# code = input("code pls?: ")
#
# new_kaomoji = Kaomoji(code)
# print(new_kaomoji)
# print(new_kaomoji.hash)
#
# while True:
#     keyword = input("Type new keyword (CTRL-C to END): ")
#     new_kaomoji.add_keywork(keyword)