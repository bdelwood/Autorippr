# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 16:08:25 2017

@author: brodi
"""
import filebot

class dbtest(object):
    def __init__(self, path, vidname,filename):
        self.vidname = vidname
        self.vidtype = "Movie"
        self.path = path
        self.filename = filename

dbvideo = dbtest("/home/brodi/Sandlot43","Sandlot43","title00.mkv")

fb = filebot.FileBot(True, False)
