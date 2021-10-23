from sys import argv

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

COMMANDS_HELP = """\
add: Add one or more comma-separated keyword(s) to the kaomoji\n
back: Go back to the kaomoji selection console\n
destroy: Delete the kaomoji from the database\n
exit: Ask to save the changes if there are changes\n then exit\n
help: Show commands (this message)\n
random: Select a random kaomoji so you can add more keywords to it\n
rm: Remove one or more comma-separated keyword(s) from the kaomoji\n
write: Backup the database and save the changes to the original\n
"""

WELCOME = """
---
Welcome. Select a kaomoji first, and then press <enter>, for example:
{console}(ヘ。ヘ)

or /random to select a random kaomoji to edit;
or /exit to exit.
---

""".format(console=CONSOLE)

INSIDE_KAOMOJI = """
You chose the kaomoji `{code}'

{status}

{commands}
"""
