#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Floyd Hightower <https://github.com/fhightower>
# May 2016
"""  . """

import sys

import argparse
import configparser
import logging

from instaparser import Instaparser


def init_parser():
    """."""
    parser = argparse.ArgumentParser(description='Get instaparser api key')
    parser.add_argument('api_key', metavar='a', type=str, nargs='?', help='Your instaparser API key')
    return parser.parse_args()


def main():
    """."""
    logging.debug("Starting main function")
    args = init_parser()

    # if there was an api key passed in as an argument, use that
    if (args.api_key):
        i = Instaparser(args.api_key)
    # if there was no api_key parameter initialize a class
    else:
        i = Instaparser()

    # use the text parser
    i.parse("https://www.biblegateway.com/passage/?search=John+1&version=NIV", "text")
    print(i.response)
    print(i.response_text['text'] + "\n\n")

    # use the article parser
    i.parse("http://genius.com/Propaganda-be-present-live-from-catalyst-atlanta-lyrics")
    print(i.response)
    print(i.response_text['description'] + "\n\n")

    # use the document parser
    i.parse("http://test.com", "document", """<!DOCTYPE HTML>
        <html>
        <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <title>test</title>
        </head>
        <body class="basic">
        <div>test-html</div>
        </body>
        </html>
        """)
    print(i.response)
    print(i.response_text['description'])

if __name__ == '__main__':
    main()
