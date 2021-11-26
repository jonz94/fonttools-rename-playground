#! /usr/bin/python

import os

from fontTools.ttLib import TTFont


def getName(nameID):
    return {
        0: "Copyright",
        1: "Family",
        2: "Styles (SubFamily)",
        3: "UniqueID",
        4: "Fullname",
        5: "Version",
        6: "Fontname",
        16: "Preferred Family",
        17: "Preferred Styles",
        18: "Compatible Full",
    }.get(nameID, "unknown")


def printsFontInfo(filename):
    font = TTFont(filename, recalcBBoxes=False)
    fontName = font["name"]

    print("========================================")
    print(f"filename: {filename}")

    for entry in fontName.names:
        encoding = (
            "utf_16_be"
            if entry.platformID == 3 and entry.platEncID in [1, 10]
            else "ascii"
        )

        print("----------------------------------------")
        print(f"nameID: {entry.nameID}, {getName(entry.nameID)}")
        print("----------------------------------------")
        if encoding == "utf_16_be":
            print(f"string: {entry.string.decode(encoding)}")
        else:
            print(f"string: {entry.string}")
        print(f"platformID: {entry.platformID}")
        print(f"platEncID: {entry.platEncID}")
        print(f"langID: {entry.langID}")

    font.close()


def rename(filename):
    font = TTFont(filename, recalcBBoxes=False)
    fontName = font["name"]

    for entry in fontName.names:
        encoding = (
            "utf_16_be"
            if entry.platformID == 3 and entry.platEncID in [1, 10]
            else "ascii"
        )

        if entry.nameID in [1, 3, 4, 16, 18]:
            entry.string = entry.string + " Nerd Font".encode(encoding)
        elif entry.nameID in [6]:
            entry.string = entry.string + "-Nerd-Font".encode(encoding)

    font.save(f"renamed-{filename}")
    font.close()


def main():
    workspace = os.environ.get("GITHUB_WORKSPACE") or os.path.abspath(__file__).replace(
        "/main.py", ""
    )

    print("\n!!! before rename !!!\n")
    for file in os.listdir(os.fsencode(workspace)):
        filename = os.fsdecode(file)
        if filename.endswith(".ttf"):
            printsFontInfo(filename)

    for file in os.listdir(os.fsencode(workspace)):
        filename = os.fsdecode(file)
        if filename.endswith(".ttf"):
            rename(filename)

    print("\n!!! after rename !!!\n")
    for file in os.listdir(os.fsencode(workspace)):
        filename = os.fsdecode(file)
        if filename.startswith("renamed-") and filename.endswith(".ttf"):
            printsFontInfo(filename)


if __name__ == "__main__":
    main()
