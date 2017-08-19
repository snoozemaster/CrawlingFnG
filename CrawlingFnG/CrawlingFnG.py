from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3 as sq
import pandas
import pandas.io.sql as pd_sql
import time


df = []
df.append(pandas.read_csv("kospi.csv",encoding='CP949'))
#df.append(pandas.read_csv("kosdaq.csv",encoding='CP949'))
select = 0  #kospi = 0, kosdaq = 1

Sym = df[select]['Symbol']
Name = df[select]['Name']
#FnG = df[select]['FnG']

conn = sq.connect("storeFnG.db")
cur = conn.cursor()  


for i in range(0,len(Sym)):
    targetURL = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode="+Sym[i]+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"
    html = urlopen(targetURL).read()
    soup = BeautifulSoup(html,'html.parser')

    try:
        fngData = soup.find("ul", {"id":"bizSummaryContent"}).getText()
        print(fngData)  
    except:
        fngData='NA'
        print("no data")

    data = (Sym[i], Name[i],fngData)
    sql = "INSERT INTO FnG(Symbol, Name, ComBrief) VALUES (?,?,?)"  
    cur.execute(sql,data)
    conn.commit()

    if(i%100==0): 
        time.sleep(5)
        print("100개마다 쉬어줍시당")

conn.close()
  
