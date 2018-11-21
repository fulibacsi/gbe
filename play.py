import argparse

from gbe.book import Book


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('bookfile', help='book file')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    book = Book(args.bookfile)
    print(book.as_str())
