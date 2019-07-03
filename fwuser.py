#coding=utf-8
__author__ = 'panwei'
import time
import telnetlib
import xmlrpclib
import re


def getserverip(prox):
    users=[]
    users=prox.getinfo()
    return users


def telnetconn(ip,user,password):
    # 连接Telnet服务器
    tn = telnetlib.Telnet(ip, port=23, timeout=50)
    tn.set_debuglevel(0)
    # 输入登录用户名
    tn.read_until('login:')
    tn.write(user + '\n')

    # 输入登录密码
    tn.read_until('password:')
    tn.write(password + '\n')
    result1 = tn.read_very_eager()
    #print result1
    return tn

def telnetgetuserip(conn,name):
    commond="get address V1-Un name %s"%(name)
    conn.write(commond + '\n')
    time.sleep(5)
    result1 = conn.read_very_eager()  # 获得结果
    comm='(%s).*?(\d.*?)/'%(name)
    searcha=re.search(comm,result1,re.I|re.M)
    #print searcha.group()
    if searcha:
        if searcha.group(1)==name and searcha.group(2)<>None:
            return searcha.group(2)
    else:
        return

def telnetcentcomm(conn,comm):
    conn.write(comm + '\n')
    time.sleep(5)
    result1 = conn.read_very_eager()  # 获得结果
    print comm
    print "\n"
    print result1
    return

if __name__ =='__main__':
    ip = '10.0.111.1'  # Telnet互联网交换机IP
    username = 'netscreen'  # 登录用户名
    password = '*******'  # 登录密码
    commond = ''
    prox = xmlrpclib.ServerProxy("http://10.0.117.11:50000", allow_none=True)
    while 1:
        users=getserverip(prox)
        telconn=telnetconn(ip,username,password)
        for user in users:
            reverse=telnetgetuserip(telconn,user['name'])
            if user['ipaddr'] <>reverse:
                comm="unset address V1-Un %s"%(user['name'])
                comm1="set address V1-Untrust %s %s/32"%(user['name'],user['ipaddr'])
                comm2="set group address V1-Un centforsoft add %s"%(user['name'])
                telnetcentcomm(telconn,comm)
                telnetcentcomm(telconn,comm1)
                telnetcentcomm(telconn,comm2)
        delusers=[]
        delusers=prox.getdeluser()
        for deluser in delusers:
            comm="unset address V1-Un %s"%(deluser['name'])
            telnetcentcomm(telconn,comm)
        telconn.close()
        users=[]
        print "sleep 60s\n"
        time.sleep(60)
