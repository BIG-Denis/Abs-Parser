
import requests
import re
from sys import argv


# silka for ABS site
wiki_url = 'https://absurdopedia.net/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:RandomInCategory/%D0%90%D0%B1%D1%81%D1%83%D1%80%D0%B4%D0%BE%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D1%8B%D0%B5_%D1%81%D1%82%D0%B0%D1%82%D1%8C%D0%B8'


# raw source function saver for debug
def raw_text(url: str) -> list:  # function out of date
    pass


# functions that return plain text
def get_text(url: str) -> list:
    url = url.replace('\n', '')
    raw_src = requests.get(url).text
    raw_src = raw_src.replace('&#160;', ' ')
    new_src = list(re.findall(pattern='<p>.*\n</p>', string=raw_src))
    new_src = [re.sub('<sup.*/sup>', '', string) for string in new_src]
    new_src = [re.sub('<[\w]*[^>]*>|</[\w]+>', '', string) for string in new_src]
    new_src = [re.sub(r'&#[0-9]+;', '', string) for string in new_src]
    new_src = [re.sub(' +', ' ', string) for string in new_src]
    return new_src


# save text function
# filename function argument without file extension
def save_text(pages: int or str, filename: str = 'text', mode: str = 'w') -> None:
    if pages.isdecimal():
        with open(f'{filename}.txt', mode) as file:
            for _ in range(int(pages)):
                file.writelines(get_text(wiki_url))
    else:
        open(f'{filename}.txt', mode).write('\n'.join([''.join(get_text(url)) for url in open(f'{pages}.txt', 'r').readlines()]))


# function for running parser from terminal
def main():
    pages, filename, mode = (None, ) * 3
    if '-p' in argv:
        pages = argv[argv.index('-p') + 1]
    if '-f' in argv:
        filename = argv[argv.index('-f') + 1]
    if '-m' in argv:
        mode = argv[argv.index('-m') + 1]
    save_text(pages, filename=filename if filename is not None else 'text', mode=mode if mode is not None else 'w')


if __name__ == '__main__':
    main()
