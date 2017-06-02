# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 14:22:11 2017

@author: brodi
"""

import tmdbsimple as tmdb
tmdb.API_KEY = "ac74d516ffdc7325420400c6df03e8f0"

search = tmdb.Search()


def query(q, dur):
    response = search.movie(query=q)
    for r in search.results:
        movie = tmdb.Movies(r['id'])
        response = movie.info()
        runtime = movie.runtime
        print type(movie.title)
        if runtime == dur:
            return movie.title
    return ""

def query_recur(q, dur):
    result = query(q, dur)
    if result and len(q.replace(" ","")) >= 4:
        return result
    else:
        return query_recur(q[:-1], dur)