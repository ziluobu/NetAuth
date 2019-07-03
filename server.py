#coding=utf-8
__author__ = 'panwei'
import sqlite3
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
import  os
info={}
conn=None


def conndb():
    global conn
    conn = sqlite3.connect('./server.db')
    db = conn.cursor()
    db.execute('''CREATE TABLE if not exists User
       (
       NAME           CHAR(20)    NOT NULL,
       IpAddr            CHAR(16)     NOT NULL,
       Pass        CHAR(20),
       Date        char(30));''')
    conn.commit()
    db.execute('''CREATE TABLE if not exists deluser
       (
       NAME           CHAR(20)    NOT NULL,
       IpAddr            CHAR(16)     NOT NULL,
       Pass        CHAR(20),
       Date        char(30),
       del         int);''')
    conn.commit()
    return conn


def insertuser(info):
    global conn
    db = conn.cursor()
    sql="INSERT INTO User (NAME,IpAddr,Pass,Date) \
      VALUES ('%s','%s', '%s',date('now'))"%(info['name'],info['ipaddr'],info['Pass'])
    db.execute(sql);
    conn.commit()

def updateuser(info):
    global conn
    db = conn.cursor()
    sql="UPDATE User set IpAddr = '%s',Pass='%s',Date=date('now') where NAME ='%s'"%(info['ipaddr'],info['Pass'],info['name'])
    db.execute(sql);
    conn.commit()


def getuser():

    global conn
    db = conn.cursor()
    user={}
    users=[]
    sql="select NAME ,IpAddr,Pass,Date from User"
    cursor=db.execute(sql)
    for row in cursor:
        user['name']=row[0]
        user['ipaddr']=row[1]
        user['Pass']=row[2]
        user['Date']=row[3]
        users.append(user)
        user={}
    return users

def namecoun(name):
    global conn
    db = conn.cursor()
    sql="SELECT count(*) as coun  from User where NAME ='%s'"%(name)
    cursor = db.execute(sql)
    for row in cursor:
        coun=row[0]
    return coun


def deluser():
    global conn
    db = conn.cursor()
    sql1="INSERT INTO deluser (NAME,IpAddr,Pass,Date,del) SELECT NAME,IpAddr,Pass,Date,0 from User where  date('now','-1 day')>=date(Date)"
    sql2="delete from User  where date('now','-1 day')>=date(Date)"
    db.execute(sql1)
    db.execute(sql2)
    conn.commit()








def updateinfo(info):
    deluser()
    coun=namecoun(info['name'])
    if coun<1:
        insertuser(info)
    else:
        updateuser(info)
    return 1

def getinfo():
    deluser()
    users=getuser()
    return users

def getdeluser():
    global conn
    db = conn.cursor()
    user={}
    users=[]
    sql="select NAME ,IpAddr,Pass,Date from deluser where del=0"
    cursor=db.execute(sql)
    for row in cursor:
        user['name']=row[0]
        user['ipaddr']=row[1]
        user['Pass']=row[2]
        user['Date']=row[3]
        users.append(user)
        user={}
    for user in users:
        sql="UPDATE deluser set del = 1 where NAME ='%s'"%(user['name'])
        db.execute(sql)
        conn.commit()
    return users


if __name__ =='__main__':
    conn=conndb()

    server = SimpleXMLRPCServer(("", 50000),requestHandler=SimpleXMLRPCRequestHandler)
    # A simple server with simple arithmetic functions
    print "Listening on port 50000... ,pid:%d"%(os.getpid())
    server.register_multicall_functions()
    server.register_function(updateinfo, 'updateinfo')
    server.register_function(getinfo, 'getinfo')
    server.register_function(getdeluser, 'getdeluser')
    server.serve_forever()


