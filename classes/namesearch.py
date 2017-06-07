# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 14:22:11 2017

@author: brodi
"""

import tmdbsimple as tmdb
import re
import wordsegment as ws
import itertools
import logger
import os
from mediainfo import get_runtime



class NameSearch(object):
    def __init__(self, config):
        self.API_Key = config['filebot']['tmdb_API']
        tmdb.API_KEY = self.API_Key
        self.search = tmdb.Search()
        self.log = logger.Logger('NameSearch', config['debug'], config['silent'])

    def database_search(self, dbvideo):
        vidname = re.sub(r'S(\d)', '', dbvideo.vidname)
        vidname = re.sub(r'D(\d)', '', vidname)
        vidpath = os.path.join(dbvideo.path, dbvideo.filename)
        self.log.debug("Attempting to find runtime.")
        runtime = get_runtime(vidpath)
        runtime = round(runtime/(60*10**3))
        self.log.info("Runtime found as {} minutes"
                       .format(runtime))
        self.log.info("Searching TheMovieDB for title matching runtime.")
        candidate = self.query(vidname, runtime)
        if candidate:
            vidname = candidate
            self.log.info("Name found: {}".format(vidname))
            return vidname
        else:
            self.log.info("Search failed. Using name obtained from disc.")
    
    def query(self, q, dur):
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
    
    
#MAybe recursion isnt rhe bes =t fo rthis job... need some way to record
# searches that already failed
#def query_recur(q, dur, forward = True):
#    result = query(q, dur)
#    print result
#    if result and len(q.replace(" ","")) >= 4:
#            print result
#            return result
#    if len(q.replace(" ","")) < 4:
#            return ""
#    else:
#        if forward:
#            print "here"
#            print q[:-1]
#            return query_recur(q[:-1], dur)
#        else:
#            print q[1:]
#            return query_recur(q[1:], dur, forward = False)
#        
#def queries(q, dur):
#    forward = query_recur(q, dur)
#    if not forward:
#        backward = query_recur(q, dur, forward = False)
#        return backward
#    return forward
    
        