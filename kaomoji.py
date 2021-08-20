from hashlib import sha256


class Kaomoji:
    """Represents a Kaomoji entity."""

    code = str()  # unicode of the kaomoji
    keywords = list()  # list of strings

    def __init__(self, code, keywords=False):

        self.code = code

        if keywords:
            self.keywords = [keyword.strip()
                             for keyword in keywords.split(',')]

        self.hash = self._makehash(code)


    def add_keyword(self, keyword):
        if not keyword in self.keywords:
            self.keywords.append(keyword.strip())


    def remove_keyword(self, keyword):
        if keyword in self.keywords:
            self.keywords.remove(keyword.strip())


    def _makehash(self, code):
        """Gives a UUID for a given kaomoji, for comparison.

        It is the base10 of the sha256 digest of the kaomoji code:
            HASH = INT10(SHA256(BYTES(UNICODE_KAOMOJI_CODE_UTF8)))

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

    # db_file = None
    filename = str()
    #kaomojis = list()
    kaomojis = dict()
    entry_num = int()


    def __init__(self, filename=None):

        if filename:

            self.filename = filename
            self.load_file(filename=filename)


    def load_file(self, filename):
        """Loads a db file."""

        self.filename = filename

        db_file = open(filename, "r")
        #with open(filename) as dbfile:
        lines = db_file.readlines()

        for line in lines:

            code, keywords = line.strip().split("\t")

            kaomoji = Kaomoji(code=code, keywords=keywords)

            self.kaomojis.update({code: kaomoji})

        self.entry_num = len(self.kaomojis)


    def write(self, filename=None):
        """Writes a db file."""

        if not filename:
            filename = self.filename

        db_file = open(filename, "w")

        for code, kaomoji in self.kaomojis.items():
            #code = kaomoji.code
            keywords_string = ", ".join(kaomoji.keywords)
            db_line = "{0}\t{1}\n".format(code, keywords_string)
            db_file.write(db_line)

        db_file.close()


    def kaomoji_exists(self, other: Kaomoji):
        """Checks if a kaomoji exists already in the database."""

        if other.code in self.kaomojis:
                return True

        return False


    def add_kaomoji(self, kaomoji: Kaomoji):
        """Adds a Kaomoji to the database."""
        self.kaomojis.update({kaomoji.code: kaomoji})

        return self.kaomojis[kaomoji.code]


    def get_kaomoji_by_code(self, code: str):
        """Gets a Kaomoji with it's current keywords from the database."""

        return self.kaomojis[code]

    def get_kaomoji_by_kaomoji(self, other: Kaomoji):
        """Gets a Kaomoji with it's current keywords from the database."""

        return self.kaomojis[other.code]

    def get_kaomoji_by_hash(self, thehash: int):
        """Gets a Kaomoji with it's current keywords from the database."""

        for kaomoji in self.kaomojis.values():
            if thehash == kaomoji.hash:
                return kaomoji

    def remove_kaomoji(self, kaomoji: Kaomoji):
        """Removes a Kaomoji from the database."""

        del self.kaomojis[kaomoji.code]


    def update_kaomoji(self, kaomoji: Kaomoji):
        """Updates keywords to database."""

        self.kaomojis.update({kaomoji.code: kaomoji})

        return self.kaomojis[kaomoji.code]
