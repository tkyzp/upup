########################################################
'''
此代码仅用于交流学习，禁止用于非法用途
'''
#######################################################

'''
从社会工程学的角度来看，up主作为B站一个小众群体，出于利益或其他原因，他们会互相关注，
形成一张庞大的关系网
理论上通过搜索引擎使用的类似算法，完全可以通过某个up爬取到所有up的关系网，
此代码使用广度优先算法，爬取b站up名单，以验证，至于对这张关系网的分析，能力不足
--2020/5/20
'''
import requests
import sqlite3
import simplejson
import time
con = sqlite3.connect('up.db')
c = con.cursor()
'''
c.execute("create table  up"
          "(mid numrber(10) primary key not null,"
          "uname varchar(10),"
          "officaialtype int );")
'''

def insert(mid:int, uname:str, officaialtype:int)->bool:
    #尝试添加进数据库,成功返回True
    try:
        c.execute('''insert into up values (?,?,?)''',(mid,uname,officaialtype))
        return True
    except:
        return False

#爬取up关注列表的api
url = 'https://api.bilibili.com/x/relation/followings?vmid={}&pn={}&ps={}&order=desc&jsonp=jsonp'


def getmid(mid,pn=1,ps=50):
    print('get {}'.format(mid))
    try:
        r = requests.get(url.format(mid,pn,ps))
        following = simplejson.loads(r.text)
        followlist = following['data']['list']
        while following['data']['total']>pn*ps:
            pn +=1
            r = requests.get(url.format(mid, pn, ps))
            time.sleep(0.5)
            following = simplejson.loads(r.text)
            if len(following['data']['list']):
                for a in following['data']['list']:
                    followlist.append(a)
        return followlist
    except:
        print('系统错误')
        time.sleep(5)
        return []
#初始化
nextlist = []
#设定从某个up开始爬取
followlist = getmid(37090048)
for follow in followlist:
    if insert(follow['mid'],follow['uname'], follow['official_verify']['type']):
        nextlist.append(follow['mid'])
while(len(nextlist)):
    for next in nextlist:
        followlist = getmid(next)
        nextlist.remove(next)
        if len(followlist):
            for follow in followlist:
                if insert(follow['mid'], follow['uname'], follow['official_verify']['type']):
                    nextlist.append(follow['mid'])
        print('commit')
        con.commit()


