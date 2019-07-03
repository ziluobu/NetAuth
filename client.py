#coding=utf-8
__author__ = 'panwei'
import sqlite3
import socket
import time
import xmlrpclib

def conndb():
    conn = sqlite3.connect('user.db')
    db = conn.cursor()
    db.execute('''CREATE TABLE if not exists User
       (
       NAME           CHAR(20)    NOT NULL,
       IpAddr            CHAR(16)     NOT NULL,
       Pass        CHAR(20));''')
    conn.commit()
    return conn

def insertdb(conn,per):
    db = conn.cursor()
    sql="INSERT INTO User (NAME,IpAddr,Pass) \
      VALUES ('%s','%s', '%s' )"%(per.name,per.ipaddr,per.Pass)
    db.execute(sql);
    conn.commit()

def readdb(conn,per):
    db = conn.cursor()
    cursor=db.execute("select NAME,IpAddr,Pass from User")
    for row in cursor:
        per.name=row[0]
        per.oipaddr=row[1]
        per.Pass=row[2]

def updatedb(conn,ipaddr):
    db = conn.cursor()
    sql="UPDATE User set IpAddr = '%s'"%(ipaddr)
    db.execute(sql);
    conn.commit()
def coundb(conn):
    db = conn.cursor()
    cursor = db.execute("SELECT count(*) as coun  from User")
    for row in cursor:
        coun=row[0]
    return coun

def getip(per):
    print "Get the native IP address\n"
    localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
    print "local ip:%s "%localIP
    #myname = socket.getfqdn(socket.gethostname())
    #per.ipaddr = socket.gethostbyname(myname)
    per.ipaddr = localIP

    return

def centip(per):
    userdata={}
    prox = xmlrpclib.ServerProxy("http://10.0.117.11:50000", allow_none=True)
    userdata['name']=per.name
    userdata['ipaddr']=per.ipaddr
    userdata['Pass']=per.Pass
    print userdata
    a=prox.updateinfo(userdata)
    return
class person():
    ipaddr=''
    oipaddr=''
    name=''
    Pass='111111'

if __name__ =='__main__':
    per= person()

    conn=None
    for num in range(1,6):
        getip(per)
        if per.ipaddr =='':
            time.sleep(10)
        else:
            break
    if per.ipaddr =='':
        exit()
    conn=conndb()
    coun=coundb(conn)

    if coun <1:
        per.name=raw_input("pinyin name\r\n")
        insertdb(conn,per)
    else:
        readdb(conn,per)
        if per.ipaddr<>per.oipaddr:
            updatedb(conn,per.ipaddr)
    centip(per)
