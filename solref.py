#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scanner
import argparse
import viewer


def main():
    scanner.index_keywords()
    try:
        parser = argparse.ArgumentParser(description='Search and open solidity reference docs.')
        parser.add_argument('keyword', nargs='?', help='keyword to search')
        parser.add_argument('-l', '--list', action='store_true', help='list all keywords')
        args = parser.parse_args()
        if args.list:
            viewer.list_all()
        elif args.keyword is not None:
            viewer.show_doc(args.keyword)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print('\tInterrupted\n')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
