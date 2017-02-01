# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 01:02:24 2017

@author: brodi
"""
import sys
import os
import autorippr
import yaml
from classes import mediainfo, logger

CONFIG_FILE = "{}/settings.cfg".format(
    os.path.dirname(os.path.abspath(__file__)))

config = yaml.safe_load(open(CONFIG_FILE))

config['debug'] = True

config['silent'] = False

log = logger.Logger("Mediatest", config['debug'], config['silent'])

filepath = os.path.dirname(sys.argv[1])
filename = os.path.basename(sys.argv[1])

dbvideo = mediainfo.dbvideo_test(filepath, filename)

forced = mediainfo.ForcedSubs(config)


log.info("Attempting to discover foreign subtitle for {}.".format(dbvideo.vidname))
track = forced.discover_forcedsubs(dbvideo)

if track is not None:
    log.info("Found foreign subtitle for {}: track {}".format(dbvideo.vidname, track))
    log.debug("Attempting to flag track for {}: track {}".format(dbvideo.vidname, track))
    flagged = forced.flag_forced(dbvideo, forced)
    if flagged:
        log.info("Flagging success.")
    else:
        log.debug("Flag failed")
else:
    log.debug("Did not find foreign subtitle for {}.".format(dbvideo.vidname))