#coding=utf-8
__author__ = 'panwei'
import xmlrpclib


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
    per.ipaddr='10.0.110.105'
    per.name='panwei'
    centip(per)