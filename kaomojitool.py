#!/usr/bin/env python3

from sys import argv

USAGE = """
Usage:
  {0} <db file name>
  If database file doesn't exist, it will be created.    

  For more info visit: https://github.com/iacchus/splatmoji-kaomoji-edit-tool
""".format(argv[0])

if len(argv) < 2:
    print(USAGE)
    exit(1)

CONSOLE = "(enter kaomoji) "
COMMAND = "(enter command)"

COMMANDS =  {
    'add': "Add one or more comma-separated keyword(s) to the kaomoji",
    'back': "Go back to the kaomoji selection console",
    'destroy': "Delete the kaomoji from the database",
    'exit': "Ask to save the changes if there are changes, then exit",
    'rm': "Remove one or more comma-separated keyword(s) to the kaomoji",
    'write': "Backup the database and save the changes to the original",
}

welcome = """
Welcome. Select a kaomoji first with the command 'kaomoji <kaomoji>', and then
press <enter> for example:

>>> (ヘ。ヘ)
"""

print(welcome)

code = input(CONSOLE)

exists = None
keywords = None
inside_kaomoji = """
You chose the kaomoji {code}

"""

command = None