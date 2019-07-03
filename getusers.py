#coding=utf-8
__author__ = 'panwei'

import xmlrpclib


def getserverip(prox):
    users=[]
    users=prox.getinfo()
    return users




if __name__ =='__main__':

    prox = xmlrpclib.ServerProxy("http://10.0.117.11:50000", allow_none=True)
    users=getserverip(prox)
    for user in users:
        print user
        print "\n"


