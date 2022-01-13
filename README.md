# RenameNhentaiFolders
Renames directory names from 'number' to 'title [artists] {parodies} (number)' where number is the nhentai number of the work. Can either take individual directories as arguments or the path of the parent directory containing intended directories. Can only traverse the immediate subdirectories of the parent.

Required packages:
- requests
- bs4 (BeautifulSoup)

```
usage: folders_nhentai_rename.py [-h] (-s SOURCE | -b BULK)

Renames directory names from 'number' to 'title [artists] {parodies} (number)' where number is the nhentai number of
the work. Can either take individual directories as arguments or the path of the parent directory containing intended
directories. Can only traverse the immediate subdirectories of the parent.

options:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        The source path(s) of each work where the name of the directory is the nhentai number.
  -b BULK, --bulk BULK  The parent directory path of the source path(s).
  ```
