# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 14:22:11 2017

@author: brodi


Additional title search operations.

    Dependencies:
        Python (nonstandard): tmdbsimple -- requires API key from TMDB, see
                              https://pypi.python.org/pypi/tmdbsimple for instructions
                              wordsegment -- a natrual language word segmentation tool
"""


import tmdbsimple as tmdb
import wordsegment as ws
import itertools
import re
import os
import logger
from mediainfo import get_runtime




class NameSearch(object):
    def __init__(self, config):
        self.API_Key = config['filebot']['tmdb_API']
        tmdb.API_KEY = self.API_Key
        self.search = tmdb.Search()
        self.log = logger.Logger('NameSearch', config['debug'], config['silent'])

    def database_search(self, dbvideo):
        """
            Wrapper function for querying the MovieDB given a Videos object. 
            
            Input:
                dbvideo (Videos): Videos object from database
                
            Output:
                If successful, returns queried name.
                else, returns None, writes to log
        """
        vidname = re.sub(r'S(\d)', '', dbvideo.vidname)
        vidname = re.sub(r'D(\d)', '', vidname)
        vidpath = os.path.join(dbvideo.path, dbvideo.filename)
        self.log.debug("Attempting to find runtime.")
        if os.path.exists(vidpath):
        runtime = get_runtime(vidpath)
            runtime = round(runtime/(60*10**3))
            self.log.info("Runtime found as {} minutes"
                           .format(runtime))
            self.log.info("Searching TheMovieDB for title matching runtime.")
            candidate = self.query(vidname, runtime)
            if candidate:
                vidname = candidate
                self.log.info("Name found: {}".format(vidname.encode('utf-8')))
                return vidname
            else:
                self.log.info("Search failed. Using name obtained from disc.")
        else:
            self.log.warn("{} does not exist".format(vidpath))
            return None
    
    def query(self, q, dur):
        """
            Performs search on the MovieDB
            
            Input: 
                q (str): Full title that needs to be matched
                dur (float): duration of that title
            
            Output:
                If query successful, matched movie title in the MovieDB.
                If not, returns empty string.
        """
        forward = []
        backward = []
        qf = q
        qr = q
        while len(qf.replace(" ","")) >= 5:
            spltf = list(qf)
            spltf.pop(0)
            forward.append("".join(spltf))
            qf = "".join(spltf)
        while len(qr.replace(" ","")) >= 5:
            spltr = list(qr)
            spltr.pop()
            backward.append("".join(spltr))
            qr = "".join(spltr)   
        tried = []
        for direction in [backward, forward]:
            for qu in direction:
                res = self.movie_search(qu, dur, tried)
                if type(res) is list:
                    tried = res
                else:
                    return res
        if q.count(" ") == 0:
            qlet = re.sub(r'\d+','', q)
            seg = ws.segment(qlet)
            for combolen in xrange(1, len(seg)):
                for combo in itertools.combinations(seg, combolen):
                    qcomb = " ".join(combo)
                    resu = self.movie_search(qcomb, dur, tried)
                    if type(resu) is list:
                        tried = resu
                    else:
                        return resu        
        return ""

    def movie_search(self, qu, dur, tried):
        """
            Performs a search of the MovieDB based on a given title and runtime.
            
            Input:
                qu (str): title to query
                dur (float): runtime of title
                tried (list): list of previously tried (and failed) queries
                
            Output:
                If query successful, matched movie title in the MovieDB
                If failed, returns mutated list of tried queries (list of 
                the MovieDB ID numbers)
        """
        response = self.search.movie(query=qu)
        for r in self.search.results:
            if r['id'] not in tried:
                tried.append(r['id'])
                movie = tmdb.Movies(r['id'])
                response = movie.info()
                runtime = movie.runtime
                if runtime == dur:
                    return movie.title
            else:
                continue
        return tried
    
    