'''
Created on 3 июня 2016 г.

@author: Михаил Булыгин <pararanax@gmail.com>
'''

from elasticsearch import Elasticsearch
from pg import DB
from pgdb import connect
from time import perf_counter as pc


if __name__ == '__main__':
    es = Elasticsearch()
    con = connect(user="postgres", password="1234", database="wiki")
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM wiki")
    count = cur.fetchone().count
    cur.execute("SELECT * FROM wiki")
    t = pc()
    for i in range(count):
        row = cur.fetchone()
        doc = {"title": row.title, "timestamp": row.timestamp, "author": row.author, "text": row.text}
        es.index(index="wiki", doc_type="article", body=doc, id=row.id)
        if i % 100 == 0:
            elapsed = pc() - t
            remaining = elapsed / (i+1) * count
            print("Elapsed: {:.0f}m {:.0f}s, Remaining: {:.0f}m {:.0f}s, Article {} of {}: {} ({:.2%})".
                  format(elapsed/60, elapsed%60, remaining/60, remaining%60, i, count, row.title, i/count))
        
    
    