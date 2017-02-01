# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 01:02:24 2017

@author: brodi
"""
import os
import autorippr
import yaml
from classes import mediainfo, logger
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('in_dir', type=str, nargs = '?')


args = parser.parse_args()



CONFIG_FILE = "{}/settings.cfg".format(
    os.path.dirname(os.path.abspath(__file__)))

config = yaml.safe_load(open(CONFIG_FILE))

config['debug'] = True

config['silent'] = False

log = logger.Logger("Mediatest", config['debug'], config['silent'])

filepath = os.path.dirname(args.in_dir)
filename = os.path.basename(args.in_dir)

dbvideo = mediainfo.dvideo_test(filepath, filename)

forced = mediainfo.ForcedSubs(config)

vidname = dbvideo.filename


log.info("Attempting to discover foreign subtitle for {}.".format(vidname))
track = forced.discover_forcedsubs(dbvideo)

if track is not None:
    log.info("Found foreign subtitle for {}: track {}".format(vidname, track))
    log.debug("Attempting to flag track for {}: track {}".format(vidname, track))
    flagged = forced.flag_forced(dbvideo, forced)
    if flagged:
        log.info("Flagging success.")
    else:
        log.debug("Flag failed")
else:
    log.debug("Did not find foreign subtitle for {}.".format(vidname))