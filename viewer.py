import os

from scanner import Doc
from scanner import KeywordsToDocMapping
from colorama import init, Fore, Back


def search_doc(arg):
    arg = arg.lower()
    matches = []
    for k in KeywordsToDocMapping.keys():
        if k.lower().startswith(arg):
            matches.append(KeywordsToDocMapping[k])
    if len(matches) == 0:
        for k in KeywordsToDocMapping.keys():
            if arg in k.lower():
                matches.append(KeywordsToDocMapping[k])
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print('Found multiple matches:\n')
        for i in range(len(matches)):
            print(Fore.GREEN + str(i) + Fore.RESET, end='')
            print(": ", end='')
            print((Fore.RED + matches[i].key + Fore.RESET).ljust(40), end=' ')
            print(matches[i].desc)
        choice = input('\nPlease select one: ')
        return matches[int(choice)]
    return None


def show_doc(arg):
    init()
    doc = search_doc(arg)
    if doc is not None:
        print(Fore.GREEN + 'Opening ' + doc.file + Fore.RESET)
        os.system('open ' + doc.file)
    else:
        print("No doc found for: " + arg)


def list_all():
    sorted_keys = sorted(KeywordsToDocMapping.keys())
    i = 0
    for k in sorted_keys:
        i += 1
        print(Fore.GREEN + str(i).rjust(2, '0') + Fore.RESET, end='')
        print(": ", end='')
        print((Fore.RED + k + Fore.RESET).ljust(40), end=' ')
        print(KeywordsToDocMapping[k].desc)
