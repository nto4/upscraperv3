

from googlesearch import search
import requests
from bs4 import BeautifulSoup as bs
import re
from bs4 import SoupStrainer
import check_mail
from urllib.parse import urlparse
import sqlite3 as sql

db_name = 'sonucdb'
data_path = "data.csv"



with open(data_path, "r") as d:
    data = d.read().splitlines()



db = sql.connect(db_name)
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS datas(key_word, url, mails, phones, c)")
cur.execute("CREATE TABLE IF NOT EXISTS errors(key_word, error)")
db.commit()
db.close()

def my(kew_word):
    x = search(kew_word, num=3, stop=3, pause=2 )
    
    x = list(x)
    # print(x)
    if len(x) > 0:
        x = x[0]
    if len(x) > 0:
        URL = urlparse(str(x)).netloc
        # print(URL)
        URL = "http://" + URL


        headersparam = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
        # print("URL")
        # print(URL)
        page_content = str(requests.get(URL, headers=headersparam).content)
        m2 = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', page_content)
        # print(m2)
        match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', page_content)
        match = set(match)
        match = list(match)
        match = check_mail.check_mails(match)
        # print(str(kew_word), end =" ")
        # print(str(URL), end =" ")
        # print(str(match), end =" ")
        m2 = set(m2)
        m2 = list(m2)

        aaa = []
        #print(m2)
        import phonenumbers
        for i in m2:
            
            x = phonenumbers.parse("+1"+str(i), None)
            if phonenumbers.is_valid_number(x):
                aaa.append(i)
        # print(str(aaa))

        db = sql.connect(db_name)
        cur = db.cursor()
        kew_word = str(kew_word)
        URL = str(URL)
        match = str(match)
        aaa = str(aaa)
        if (len(kew_word) > 0) and (len(URL) >0) and (match != "[]") and (aaa != "[]"):
            c = "OK"
        else:
            c = "NO"
        cur.execute("INSERT INTO datas(key_word, url, mails, phones, c) VALUES (?,?,?,?,?) ",( kew_word,URL,match,aaa,c ) )
        db.commit()
        # cur.execute("SELECT * FROM datas")
        # rows = cur.fetchall()
        # print(rows)

    else:

        print("cant find url")
# my(kew_word)

for i in data:
    try:
        my(i)
    except Exception as e:
        ee = str(e)
        db = sql.connect(db_name)
        cur = db.cursor()
        cur.execute("INSERT INTO errors(key_word, error) VALUES (?,?) ",( i,ee ) )
        db.commit()
        print(e)


db = sql.connect(db_name)
cur = db.cursor()

cur.execute("SELECT * FROM datas")
rows = cur.fetchall()
print(rows)

print("*"*80)
cur.execute("SELECT * FROM errors")
rows = cur.fetchall()
print(rows)


# my("DIFFERENT HANDS")