#!/usr/bin/env python3

from sys import argv
import time

from kaomoji import Kaomoji
from kaomoji import KaomojiDB

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

    def __init__(self, db, kaomoji):
        self.db = db
        self.kaomoji = kaomoji


    def add(self, args):
        keywords = args.split(",")
        for keyword in keywords:
            self.kaomoji.add_keyword(keyword)

    def back(self):
        pass

    def backup_db(self):

        timestamp = time.time()
        backup_filename = "{filename}.{timestamp}.bkp"\
            .format(filename=self.db.filename, timestamp=timestamp)

        backup = KaomojiDB(filename=self.db.filename)
        backup.write(filename=backup_filename)

    def destroy(self):
            self.db.remove_kaomoji(self.kaomoji)


    def exit(self):

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
        pass

    # elif args[0] == "random":
    #     pass

    def rm(self, args):
        # elif args[0] == "rm":
        keywords = args.split(",")
        for keyword in keywords:
            self.kaomoji.remove_keyword(keyword)

    def write(self):

        self.db.write()

if len(argv) < 2:
    print(USAGE)
    exit(1)

filename = argv[1]
db = KaomojiDB(filename=filename)

# kaomoji selection
while True:

    print(WELCOME)

    # prompt 1
    code = input(CONSOLE)

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
    while True:

        selected_kaomoji = Kaomoji(code)

        if db.kaomoji_exists(selected_kaomoji):
            kaomoji = db.get_kaomoji_by_code(code)
            num = len(kaomoji.keywords)
            status = "The selected kaomoji exists on the database and has" \
                     " currently {num} keywords: {keywords}" \
                .format(num=num, keywords=", ".join(kaomoji.keywords))
        else:
            status = "New kaomoji! Not on the database currently."
            kaomoji = db.add_kaomoji(selected_kaomoji)

        inside_kaomoji = INSIDE_KAOMOJI.format(code=code, status=status,
                                               commands=COMMANDS_HELP)

        print(inside_kaomoji)

        # prompt 2
        command_line = input(COMMAND)

        command, *args = command_line.split(" ", maxsplit=1)
        args = " ".join(args)

        # let's instantiate our interface for given commands
        interface = KaomojiTool(db=db, kaomoji=kaomoji)

        #
        # ADD
        #
        if command == "add":
            interface.add(args)

        #
        # BACK
        #
        elif command == "back":
            break

        #
        # DESTROY
        #
        elif command == "destroy":
            option = input("Delete the kaomoji from database? (y/N) ")
            if option in ('Y', 'y'):
                interface.destroy()
            break

        #
        # EXIT
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
        # HELP
        #
        elif command == "help":
            continue

        #
        # RANDOM
        #
        # THIS IS BEING THOUGH OF BEING IMPLEMENTED SO WE CAN TAG BETTER SOME
        # KAOMOJIS WHICH AREN'T BEING
        #
        # elif args[0] == "random":
        #     pass

        #
        # RM
        #
        elif command == "rm":
            interface.rm(args=args)

        #
        # WRITE
        #
        elif command == "write":

            print("Backing up database...")
            interface.backup_db()

            print("Writing database...")
            interface.write()