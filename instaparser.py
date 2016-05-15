#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Floyd Hightower <https://github.com/fhightower>
# May 2016
"""Python wrapper for Instaparser API (https://www.instaparser.com/)."""

import configparser
import json
import logging
import requests
import sys

_BASE_URL = "https://www.instaparser.com"
_API_VERSION = "api/1"
_PARSERS = ["article", "document", "text"]


class Instaparser(object):
    """Instaparser class."""

    def __init__(self, api_key=None):
        """Initialize an instaparser instance."""
        logging.debug("Initializing an instaparser instance")
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = self._read_api_key()

    def _read_api_key(self):
        """If no api key is specified, try to read the api key from the instaparser.conf file."""
        logging.debug("Reading api key from instaparser.conf")
        try:
            config = configparser.RawConfigParser()
            config.read("instaparser.conf")
            api_key = config.get("instaparser", "api_key")
        except configparser.NoSectionError as e:
            logging.error("Unable to read the api key from instaparser.conf")
            sys.exit(1)
        else:
            return api_key

    def parse(self, url, parser="article", html=""):
        """Use instaparser to parse a url."""
        parser = parser.lower()
        logging.debug("Begining instaparser parsing of {} with the {} parser".format(url, parser))

        if parser not in _PARSERS:
            logging.error("Parser {} is not of the available parsers via instaparser (please use 'article', 'document', 'or text')".format(parser))
            sys.exit(1)

        data = {'api_key': self.api_key, 'url': url}
        # handle the documents api
        if parser == "document":
            body = {'html': html}
            response = requests.post("/".join([_BASE_URL, _API_VERSION, parser]), params=data, data=body)
        # handle the text and article apis
        else:
            response = requests.get("/".join([_BASE_URL, _API_VERSION, parser]), params=data)

        if response.ok:
            self.response = response
            self.response_text = json.loads(response.text)
        else:
            logging.error("Response from instaparser is NOT ok: {}".format(response))
            sys.exit(1)
