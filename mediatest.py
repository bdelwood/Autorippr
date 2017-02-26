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
lang = 'en'

from pymediainfo import MediaInfo
import pipes
MEDIADIR = args.in_dir
media_info = MediaInfo.parse(MEDIADIR)
#print 'tracks:', media_info.tracks
subs = []
for track in media_info.tracks:
    data = track.to_data()
    print data["track_type"]
    if data['track_type'] == 'Text' and data['language'] == lang:
        subs.append(data)
    print subs
        
#   Sort list by size of track file
    subs.sort(key=lambda sub: sub['stream_size'], reverse = True)

#   Main language subtitle assumed to be largest
    main_sub = subs[0]
    main_subsize = main_sub['stream_size']
    main_sublen = float(main_sub['duration'])
#   Checks other subs for size, duration, and if forced flag is set
    for sub in subs[1:]:
        if (
            sub['stream_size'] <= main_subsize*.1
            and main_sublen*.9 <= float(sub['duration']) <= main_sublen*1.1
            and sub['forced']=='No'
            ):
            secondary_sub = sub
        else:
            log.info("No foreign language subtitle found, try adjusting ratio.")
    print secondary_sub['track_id']


#if track is not None:
#    log.info("Found foreign subtitle for {}: track {}".format(vidname, track))
#    log.debug("Attempting to flag track for {}: track {}".format(vidname, track))
#    flagged = forced.flag_forced(dbvideo, forced)
#    if flagged:
#        log.info("Flagging success.")
#    else:
#        log.debug("Flag failed")
#else:
#    log.debug("Did not find foreign subtitle for {}.".format(vidname))

del autorippr.me