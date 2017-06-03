# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 14:22:11 2017

@author: brodi
"""

import tmdbsimple as tmdb
tmdb.API_KEY = "ac74d516ffdc7325420400c6df03e8f0"

search = tmdb.Search()


def query(q, dur):
    forward = []
    backward = []
    qf = q
    qr = q
    while len(qf.replace(" ","")) >= 5:
        spltf = list(qf)
        spltf.pop(0)
        forward.append("".join(spltf))
        qf = "".join(spltf)
        print qf
    while len(qr.replace(" ","")) >= 5:
        spltr = list(qr)
        spltr.pop()
        backward.append("".join(spltr))
        qr = "".join(spltr)   
    tried = []
    for direction in [backward, forward]:
        for q in direction:
            response = search.movie(query=q)
            for r in search.results:
                if r['id'] not in tried:
                    tried.append(r['id'])
                    movie = tmdb.Movies(r['id'])
                    response = movie.info()
                    runtime = movie.runtime
                    if runtime == dur:
                        return movie.title
        else:
            continue
    return ""

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
    
        