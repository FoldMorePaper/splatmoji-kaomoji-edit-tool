#!/usr/bin/env python3

from sys import argv
import time
import random

from kaomoji import *
from env_vars import *


class KaomojiTool:
    """ This class implements facilities for interacting with the command line
            interface.
    """
    # kaomoji global var Kamomoji()
    # db global var KaomojiDB()
    changes_made = False

    def __init__(self, db):
        """ Opens the database and selects the user-selected kaomoji for
                editing it inside the database.
        """

        self.db = db

    def add(self, args):
        """ Implements the `add` command; adds keywords to the selected kaomoji.
        """
        try:
            keywords = args.split(",")
            for keyword in keywords:
                # self.db.kaomojis[self.kaomoji.code].add_keyword(keyword)
                self.kaomoji.add_keyword(keyword)
            self.changes_made = True
        except:
            self.changes_made = False

    # TODO: def back(self):

    def backup_db(self):
        """Creates a backup of the database before rewriting it."""

        timestamp = time.time()
        backup_filename = "{filename}.{timestamp}.bkp"\
            .format(filename=self.db.filename, timestamp=timestamp)

        backup = KaomojiDB(filename=self.db.filename)
        backup.write(filename=backup_filename)

    def destroy(self):
        option = input("Delete the kaomoji `{}' from database? (y/N) "
                       .format(code))
        if option in ('Y', 'y'):
            self.db.remove_kaomoji(self.kaomoji)
            print("Backing up database...")
            self.backup_db()
            print("Writing database...")
            self.write()
            return True  # break
        if option in ('N', 'n'):
            return False  # continue
        else:
            print("Doing nothing as the answer was invalid.")
            return False  # continue

    def exit(self):
        """Exits the command line interface."""
        if changes_made:
            option = input("Save changes? (y/n) ")

            if option in ('Y', 'y'):
                print("Backing up database...")
                self.backup_db(db=self.db)

                print("Writing database...")
                self.db.write()
                self.changes_made = False
                exit(0)

            elif option in ('N', 'n'):
                exit(0)

            print("Doing nothing as the answer was invalid.")
            return False
        else:
            exit(0)

        # inside kaomoji
        # NOTE: the only two important variables we receive here are `db` and
        #       `kaomoji`; we can easily encapsulate these code below inside
        #        a function or a class then. Maybe to be done.
        #
        # Implements the second prompt, this is, inside the chosen kaomoji, with
        #   commands in respect to it.
    def set_kaomoji(self, kaomoji):
        self.kaomoji = kaomoji

    def check_kaomoji(self, code):
        # If the kaomoji exists, loads it with the current keywords it have in
        #   the database;
        # If it doesn't exists, then create it.
        if self.db.kaomoji_exists(self.kaomoji):
            #kaomoji = db.get_kaomoji_by_code(code)
            self.kaomoji = self.db.kaomojis[code]
            num = len(self.kaomoji.keywords)
            status = "The selected kaomoji exists on the database and has" \
                " currently {num} keywords: {keywords}" \
                .format(num=num, keywords=", ".join(self.kaomoji.keywords))
        else:
            self.kaomoji = self.db.add_kaomoji(self.kaomoji)
            #kaomoji = db.kaomojis.update({selected_kaomoji.code: list()})
            changes_made = True  # a new kaomoji is being added
            status = "New kaomoji! Not on the database currently."
        return status

    def get_random_kaomoji(self):
        random_kaomoji = random.choice(list(self.db.kaomojis.keys()))
        return random_kaomoji

    def help(self):
        """Shows help; help is show after every command, so doing nothing shows
                the help menu with the commands.
        """

        pass

    # elif args[0] == "random":
    #     pass

    def rm(self, args):
        """ Implements the `rm` command; removes keywords to the selected
                kaomoji.
        """
        try:
            keywords = args.split(",")
            for keyword in keywords:
                self.kaomoji.remove_keyword(keyword)

            print(tool.db.kaomojis[tool.kaomoji.code].keywords)
            self.changes_made = True
        except:
            self.changes_made = False

    def write(self):
        print("Backing up database...")
        self.backup_db()

        print("Writing database...")
        self.db.write()
        self.changes_made = False


if len(argv) < 2:  # If we don't have a database file via second argument, ask
    #     for it
    print(USAGE)
    exit(1)

filename = argv[1]
# instanciate a KaomojiTool with an instance of KaomojiDB using the db file.
tool = KaomojiTool(KaomojiDB(filename=filename),)


###################################################################################################
# ---- Menu >>--->> kaomoji selection menu first neet to select a kaomoji-------------------------#
###################################################################################################
def menu():

    print(WELCOME)

    code = input(CONSOLE).strip()

    if code == "/random":
        code = tool.db.get_random_kaomoji()

    # implements the `/exit` command in the kaomoji selection prompt
    elif (code == "/exit") | (code == "exit"):
        tool.exit()
###################################################################################################
# ---- end of the selection menu section >>----------->> kaomoji action menu ---------------------#
###################################################################################################
    while True:
        # set the selected kaomoji on the tool so we can manage it inside it
        tool.set_kaomoji(Kaomoji(code))
        status = tool.check_kaomoji(code)

        # Shows the prompt to the selected kaomoji, with the commands.
        inside_kaomoji = INSIDE_KAOMOJI.format(
            code=code, status=status, commands=COMMANDS_HELP)
        print(inside_kaomoji)

        # Shows the seleted kaomoji with it's current keywords.
        repr(tool.kaomoji)

        # prompt 2
        # shows the command prompt
        command_input = input(COMMAND)
        print(status)

        # gets the command and its arguments
        command, *args = command_input.split(" ", maxsplit=1)
        args = " ".join(args)
###################################################################################################
# ---- commands execution ------------------------------------------------------------------------#
###################################################################################################
        # The `ADD` command
        # command usage:
        #   add keyword1, keyword 2, etc, etcc
        #
        if command == "add":
            tool.add(args)

        # The `BACK` command, gets you back to the selection menu
        # command usage:
        #   back
        #
        elif command == "back":
            break

        # The `DESTROY` command removes selected kaomoji from the database and writes it to file
        # command usage:
        #   destroy
        #
        elif command == "destroy":
            if tool.destroy():
                break
            else:
                continue

        # the `EXIT` command
        # command usaage:
        #   exit
        #
        elif command == "exit":
            tool.exit()

        # The `HELP` command: just waits the help to be shown at the beggining.
        # command usage:
        #   help
        #
        elif command == "help":
            continue

        # The `RANDOM` command, selects a new random kaomoji
        # command usage:
        #   random
        #
        elif command == "random":
            code = tool.get_random_kaomoji()

        # The `RM` command removes keywords from the selected kaomoji
        # command usage:
        #   rm keyword1, keyword 2, etc, etcc
        #
        elif command == "rm":
            tool.rm(args=args)

        # The `WRITE` command will write changes to db file
        # command usage:
        #   write
        #
        elif command == "write":
            tool.write()


while True:
    menu()
