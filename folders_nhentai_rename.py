import sys
import os
import requests
import argparse
from bs4 import BeautifulSoup


TITLE_DELIM_CHAR_ORD = 187 # »
URL_BASE = "https://nhentai.net/g/"


def GenerateUrl(number):
    url = URL_BASE + number + "/"
    return url

def GetText(url):
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    text = html.get_text()
    return text

def GetTitle(text):
    title = text.split(chr(TITLE_DELIM_CHAR_ORD))
    title = title[0].replace('\t', '').replace('\n', '').replace('/', ' ').replace('\\', ' ')
    return title

def GetArtists(text):
    if 'Artists:' in text:
        artist = "".join(filter(lambda x: not x.isdigit(), text.split('Artists:')[1].replace('\t', '').split('\n')[1]))
        artist = RemoveTrailingCharacters(artist)
        return artist
    else:
        return 0

def GetParodies(text):
    if 'Parodies:' in text:
        parody = "".join(filter(lambda x: not x.isdigit(), text.split('Parodies:')[1].replace('\t', '').split('\n')[1]))
        parody = RemoveTrailingCharacters(parody)
        return parody
    else:
        return 0

def RemoveTrailingCharacters(text):
    if text != '':
        if text[-1] == 'K':
            return text[:-1]

    return text

def GetNewName(number, text):
    # TITLE [Artists:] {Parodies:} (NUMBER)
    title = GetTitle(text)
    artist = GetArtists(text)
    parody = GetParodies(text)

    if artist != '':
        artist = " [" + artist + "]"
    if parody != '':
        parody = " {" + parody + "}"

    return title + artist + parody + " (" + number + ")"



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Renames directory names from 'number' to 'title [artists] {parodies} (number)' where number is the nhentai number of the work. Can either take individual directories as arguments or the path of the parent directory containing intended directories. Can only traverse the immediate subdirectories of the parent.")
    sourceGroup = parser.add_mutually_exclusive_group(required=True)
    sourceGroup.add_argument("-s", "--source", action="append", type=str, help="The source path(s) of each work where the name of the directory is the nhentai number.")
    sourceGroup.add_argument("-b", "--bulk", type=str, help="The parent directory path of the source path(s).")

    args = parser.parse_args()

    invalidFolderFlag = False

    if args.bulk:
        if os.path.isdir(args.bulk):
            pathList = [f.path for f in os.scandir(args.bulk) if f.is_dir()]

            if not pathList:
                print("No subdirectories found in: '" + args.bulk + "'")
                sys.exit()

            for path in pathList:
                numbers = os.path.basename(path)
                number = numbers.split(" ")[0]

                if number.isdigit():
                    url = GenerateUrl(number)
                    text = GetText(url)
                    newName = GetNewName(numbers, text)
                    os.rename(path, os.path.join(args.bulk, newName))
                    print(newName)

                else:
                    invalidFolderFlag = True

            if invalidFolderFlag:
                print("Not all subdirectories were nhentai numbers. Those directories have been ignored.")

        else:
            print("'" + args.bulk + "' is an invalid directory path. Program terminated.")
            sys.exit()
    else:
        for path in args.source:
            if os.path.isdir(path):
                numbers = os.path.basename(path)
                number = numbers.split(" ")[0]

                if number.isdigit():
                    url = GenerateUrl(number)
                    text = GetText(url)
                    newName = GetNewName(numbers, text)
                    os.rename(path, os.path.join(args.bulk, newName))
                    print(newName)

                else:
                    invalidFolderFlag = True
            else:
                print("'" + path + "' is an invalid directory path and has been ignored.")

        if invalidFolderFlag:
            print("Not all subdirectories were nhentai numbers. Those directories have been ignored.")






#
