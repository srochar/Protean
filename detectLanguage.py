#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'srocha'

from PatterProtean import detectLanguage,getPatterProtean
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f",'--file',
                        dest="filename",
                        help="File",
                        metavar="FILE")
    parser.add_argument("-e",'--encoding',
                        dest="encoding",
                        help="encoding to file",
                        default='utf-8')
    parser.add_argument("-a", "--all",
                        dest="all",
                        help="all language detectec",
                        action="store_true",
                        default=False)

    args = parser.parse_args()
    try:
        file = open(args.filename, 'r',encoding=args.encoding)
        patterProtean = getPatterProtean(file.read())
        lanaguages = detectLanguage(patterProtean)
        allLanguage = args.all
        if allLanguage:
           print(lanaguages)
        else:
           print(max(lanaguages))

    except LookupError as e:
        print (e)
