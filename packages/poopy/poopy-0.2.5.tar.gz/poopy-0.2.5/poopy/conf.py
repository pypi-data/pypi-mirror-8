#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <jbc.develop@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY in return Juan BC


#==============================================================================
# DOCS
#==============================================================================

"""This module create and mantain the basic Poopy configuration

"""


#==============================================================================
# IMPORTS
#==============================================================================

import os
import uuid
import json
import logging
import collections

try:
    import cPickle as pickle
except ImportError:
    import pickle

from . import PRJ, STR_VERSION

#==============================================================================
# CONSTANTS
#==============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

USER_HOME = os.path.expanduser("~")

POOPY_DIR = os.path.join(USER_HOME, ".poopy")

CONF_PATH = os.path.join(POOPY_DIR, "conf.json")

POOPY_FS = os.path.join(POOPY_DIR, "poopy_fs")

SCRIPTS = os.path.join(POOPY_DIR, "scripts")


#==============================================================================
# LOGGER
#==============================================================================

log_level = logging.DEBUG

def getLogger(name=PRJ):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter(
        '[%(levelname)s|%(asctime)s] %(name)s > %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


#==============================================================================
# CONFS
#==============================================================================

def conf_from_file(conf_path=CONF_PATH):
    data = None
    if not os.path.isdir(os.path.dirname(conf_path)):
        os.makedirs(os.path.dirname(conf_path))
    if os.path.exists(conf_path):
        with open(conf_path) as fp:
            data = json.load(fp)
    else:
        data = {
            "UUID": unicode(uuid.uuid4()),
            "POOPY_FS": POOPY_FS,
            "SCRIPTS":  SCRIPTS,
            "TTL": 30,
            "SLEEP": 5,
        }
        with open(conf_path, "w") as fp:
            json.dump(data, fp, indent=2)
    data["CONF_PATH"] = conf_path
    return conf(**data)


def conf(**kwargs):
    cls = collections.namedtuple("Conf", kwargs.keys())
    return cls(**kwargs)


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)




