#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scanner
import argparse
import viewer
import os


def main():
    try:
        parser = argparse.ArgumentParser(description="Search and open reference docs.")
        parser.add_argument("keyword", nargs="?", help="keyword to search")
        parser.add_argument(
            "-l", "--list", action="store_true", help="list all keywords"
        )
        parser.add_argument("-d", "--doc", help="the folder path of documents")
        args = parser.parse_args()

        if args.doc is None:
            scanner.DOC_DIR = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "docs"
            )
        else:
            scanner.DOC_DIR = args.doc

        scanner.index_keywords()

        if args.list:
            viewer.list_all()
        elif args.keyword is not None:
            viewer.show_doc(args.keyword)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\tInterrupted\n")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
