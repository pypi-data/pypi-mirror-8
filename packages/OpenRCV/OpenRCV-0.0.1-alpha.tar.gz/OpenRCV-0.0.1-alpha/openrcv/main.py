#!/usr/bin/env python

"""
This module houses the "highest-level" programmatic API.

"""

import sys

from openrcv import models
from openrcv.models import BallotList
from openrcv.parsing import BLTParser
from openrcv.utils import FILE_ENCODING


def do_parse(ballots_path, encoding=None):
    if encoding is None:
        encoding = FILE_ENCODING

    contests = []
    for count in range(3, 6):
        contest = models.random_contest(count)
        contests.append(contest)
    
    contests_obj = [c.__jsobj__() for c in contests]

    tests_jobj = {
        "_version": "0.1.0-alpha",
        "contests": contests_obj
    }
    json = models.to_json(tests_jobj)

    print(json)
    exit()
    parser = BLTParser()
    info = parser.parse_path(ballots_path)
    print(repr(info))
