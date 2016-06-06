'''
Created on 1 июня 2016 г.

@author: Михаил Булыгин <pararanax@gmail.com>
'''
import xml.etree.ElementTree as ET
from pg import DB


if __name__ == '__main__':
    file = open("ruwiki.xml", encoding="utf-8")
    tree = ET.iterparse(file)
    
    db = DB(host="localhost", user="postgres", passwd="1234", dbname="wiki")
    db.query("TRUNCATE TABLE wiki")
    
    for i, line in enumerate(tree):
        event, element = line
        if element.tag == "page":
            pageid = element.find("id").text
            title = element.find("title").text
            timestamp = element.find("revision").find("timestamp").text.replace("T", " ")
            username = element.find("revision").find("contributor").find("username")
            if not username is None:
                author = username.text
            else:
                author = element.find("revision").find("contributor").find("ip").text
            text = element.find("revision").find("text").text
            
            db.insert("wiki", id=pageid, title=title, timestamp=timestamp, author=author, text=text)
            
            if i % 10**4 == 0:
                print(round(i/10**6 / 14.8 * 100, 2), "%", pageid, title, timestamp, author)
    
    print(db.query("SELECT id, title, timestamp, author FROM wiki"))