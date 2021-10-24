# Splatmoji - Kaomoji db editor

## Features:

* easily add new kaomoji to the database with the splatmoji format*
* easily add or remove new keywords

## Usage:

Run `kaomojitool.py /path/to/tsv/database/file.tsv`

if you want to use it to edit the db from the project splatmoji run: 

`kaomojitool.py /usr/share/splatmoji/data/emoticons/emoticons.tsv`

input an comand

**command list:**
- help : Show commands (this message).
- add : Add one or more comma-separated keyword(s) to the kaomoji.
- back : Go back to the kaomoji selection console.
- destroy : Delete the kaomoji from the database.
- exit : Ask to save the changes if there are changes. then exit.
- random : Select a random kaomoji so you can add more keywords to it.
- rm : Remove one or more comma-separated keyword(s) from the kaomoji.
- write : Backup the database and save the changes to the original.

## The splatmoji db format:

The [splatmoji](https://github.com/cspeterson/splatmoji) project uses a .tsv file (tab separated values) file as the db, but as we all know file extensions mean nothing about the content of itself, they are just a suggestion. And it is the casse with the splatmoji format, soince its a mixed format between tsv and csv(comma separated values).

the splatmoji db format, uses two columns on the tsv, kaoji and keys, where keys ar all the keys for the kaomoji, but instead of using tsv to sepparate the single keys, uses a csv format.

splatmoji db example:
```tsv
UwU cute,kawaii
OwO surprise,cute
|_・)  hide,creep,stare
```
### But why TSV?
TSV is required to store kaomoji on a file, along with other data in the same file, since tabs is the only character that you **won't** find in a kaomoj, since it's size varies, so the kaomoji would not be consistant.

### Why not pure TSV instead of a mixed format?

Is uncertain why the developers of splatmoji decided it that way, but its certeanly a awful parsing that mixed format. We would rather splatmoji to switch to a pure tsv format instead.

## Upcommings!
One of the maintainers from this project; [**zark0**](https://github.com/zark0-UwU) is porting this project on a **branch** to a more refined and featured version with a language which is more apropiate, currently the idea is porting to **GO**, but may change to **Rust**.

Please keep in mind that the original python code will stay on this repo, and will be supported for bugfixes, but I strongly doubt, that any aditional feature will be added to this version.
