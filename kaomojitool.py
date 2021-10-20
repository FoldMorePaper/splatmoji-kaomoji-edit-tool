#!/usr/bin/env python3

from sys import argv
import time

from kaomoji import Kaomoji
from kaomoji import KaomojiDB

import random

def backup_db(db: KaomojiDB):

    timestamp = time.time()
    backup_filename = "{filename}.{timestamp}.bkp".format(filename=db.filename,
                                                          timestamp=timestamp)
    backup = KaomojiDB(filename=db.filename)
    backup.write(filename=backup_filename)

USAGE = """
Usage:
  {0} <db file name>
  If database file doesn't exist, it will be created.    

  For more info visit: https://github.com/iacchus/splatmoji-kaomoji-edit-tool
""".format(argv[0])

# PROMPTS
CONSOLE = "(enter kaomoji) "
COMMAND = "(enter command) "
RANDOM = "(enter a comma-separated list of keywords; /next to next," \
         " /exit to exit) "

COMMANDS =  {
    'add': "Add one or more comma-separated keyword(s) to the kaomoji",
    'back': "Go back to the kaomoji selection console",
    'destroy': "Delete the kaomoji from the database",
    'exit': "Ask to save the changes if there are changes, then exit",
    "help": "Show commands (this message)",
    'random': "Select a random kaomoji so you can add more keywords to it",
    'rm': "Remove one or more comma-separated keyword(s) from the kaomoji",
    'write': "Backup the database and save the changes to the original",
}

COMMANDS_HELP = str()
COMMANDS_HELP = """\
List of commands for the selected kaomoji/database:\n
"""
for command, description in COMMANDS.items():
    COMMANDS_HELP += "{command}: {description}\n"\
        .format(command=command, description=description)

WELCOME = """
---
Welcome. Select a kaomoji first, and then press <enter>, for example:
{console}(ヘ。ヘ)

or /exit to exit.
---

""".format(console=CONSOLE)

INSIDE_KAOMOJI = """
You chose the kaomoji {code}

{status}

{commands}
"""

class KaomojiTool:
    """ This class implements facilities for interacting with the command line
            interface.
    """

    def __init__(self, db, kaomoji):
        """ Opens the database and selects the user-selected kaomoji for
                editing it inside the database.
        """

        self.db = db
        self.kaomoji = kaomoji


    def add(self, args):
        """ Implements the `add` command; adds keywords to the selected kaomoji.
        """

        keywords = args.split(",")
        for keyword in keywords:
            #self.db.kaomojis[self.kaomoji.code].add_keyword(keyword)
            self.kaomoji.add_keyword(keyword)

    # def back(self):
    #     pass

    def backup_db(self):
        """Creates a backup of the database before rewriting it."""

        timestamp = time.time()
        backup_filename = "{filename}.{timestamp}.bkp"\
            .format(filename=self.db.filename, timestamp=timestamp)

        backup = KaomojiDB(filename=self.db.filename)
        backup.write(filename=backup_filename)

    def destroy(self):
        self.db.remove_kaomoji(self.kaomoji)
        #del self.kaomoji



    def exit(self):
        """Exists the command line interface."""

        option = input("Save changes? (y/n) ")

        if option in ('Y', 'y'):
            print("Backing up database...")
            backup_db(db=self.db)

            print("Writing database...")
            self.db.write()

            exit(0)

        elif option in ('N', 'n'):
            exit(0)

        print("Doing nothing as the answer was invalid.")

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

        keywords = args.split(",")
        for keyword in keywords:
            self.kaomoji.remove_keyword(keyword)

    def write(self):

        self.db.write()

if len(argv) < 2:  # If we don't have a database file via second argument, ask
                   #     for it

    print(USAGE)
    exit(1)

filename = argv[1]
db = KaomojiDB(filename=filename)  # populate out KaomojiDB class with
                                   #     the db file.

# kaomoji selection
while True:

    print(WELCOME)

    # prompt 1
    # prompts to enter a kaomoji - be it already existing or to be created.
    code = input(CONSOLE).strip()

    # implements the `/exit` command in the kaomoji selection prompt
    if code == "/exit":
        option = input("Save changes? (y/n) ")

        if option in ('Y', 'y'):
            print("Backing up database...")
            backup_db(db=db)

            print("Writing database...")
            db.write()

            exit(0)

        elif option in ('N', 'n'):
            exit(0)

        print("Doing nothing as the answer was invalid.")
        continue

    # inside kaomoji
    # NOTE: the only two important variables we receive here are `db` and
    #       `kaomoji`; we can easily encapsulate these code below inside
    #        a function or a class then. Maybe to be done.
    #
    # Implements the second prompt, this is, inside the chosen kaomoji, with
    #   commands in respect to it.
    while True:

        selected_kaomoji = Kaomoji(code)

        # If the kaomoji exists, loads it with the current keywords it have in
        #   the database;
        # If it doesn't exists, then create it.
        if db.kaomoji_exists(selected_kaomoji):
            #kaomoji = db.get_kaomoji_by_code(code)
            kaomoji = db.kaomojis[code]
            num = len(kaomoji.keywords)
            status = "The selected kaomoji exists on the database and has" \
                     " currently {num} keywords: {keywords}" \
                .format(num=num, keywords=", ".join(kaomoji.keywords))
        else:
            status = "New kaomoji! Not on the database currently."
            kaomoji = db.add_kaomoji(selected_kaomoji)
            #kaomoji = db.kaomojis.update({selected_kaomoji.code: list()})

        # Shows the prompt to the selected kaomoji, with the commands.
        inside_kaomoji = INSIDE_KAOMOJI.format(code=code, status=status,
                                               commands=COMMANDS_HELP)

        print(inside_kaomoji)

        # Shows the seleted kaomoji with it's current keywords.
        repr(kaomoji)

        # prompt 2
        # prompts for the command
        command_line = input(COMMAND)

        # gets the command and its arguments
        command, *args = command_line.split(" ", maxsplit=1)
        args = " ".join(args)

        # let's instantiate our interface for executing the given commands
        #   This is done again after each command is issued.
        interface = KaomojiTool(db=db, kaomoji=kaomoji)

        #
        # The `ADD` command
        #
        # command usage:
        #   add keyword1, keyword 2, etc, etcc
        #
        if command == "add":
            interface.add(args)

        #
        # The `BACK` command
        #
        # command usage:
        #   back
        #
        elif command == "back":
            break

        #
        # The `DESTROY` command
        #
        # command usage:
        #   destroy
        #
        elif command == "destroy":
            option = input("Delete the kaomoji from database? (y/N) ")
            if option in ('Y', 'y'):
                interface.destroy()
                print("Backing up database...")
                interface.backup_db()
                print("Writing database...")
                interface.write()
                break
            if option in ('N', 'n'):
                continue
            else:
                print("Doing nothing as the answer was invalid.")
                continue

        #
        # the `EXIT` command
        #
        # command usaage:
        #   exit
        #
        elif command == "exit":

            option = input("Save changes? (y/n) ")

            if option in ('Y', 'y'):

                print("Backing up database...")
                interface.backup_db()

                print("Writing database...")
                interface.write()

                exit(0)

            elif option in ('N', 'n'):
                exit(0)

        #
        # The `HELP` command
        #
        # command usage:
        #   help
        #
        elif command == "help":
            continue

        #
        # The `RANDOM` command
        #
        # command usage:
        #   random
        #
        elif command == "random":
            chosen_random = random.choice(list(db.kaomojis.keys()))
            code = chosen_random
            continue

        #     pass

        #
        # The `RM` command
        #
        # command usage:
        #   rm keyword1, keyword 2, etc, etcc
        #
        elif command == "rm":
            interface.rm(args=args)
            print(db.kaomojis[kaomoji.code].keywords)

        #
        # The `WRITE` command
        #
        # command usage:
        #   write
        #
        elif command == "write":

            print("Backing up database...")
            interface.backup_db()

            print("Writing database...")
            interface.write()