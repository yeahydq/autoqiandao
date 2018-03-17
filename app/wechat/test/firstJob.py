# -*- coding: UTF-8 -*-
import itchat, time
import pickle
import sys
GLOBAL_COOKIES_FILENAME='/tmp/wechat_cookies'


def lc():
  print("Finash Login!")
def ec():
  print("exit")

#
# with open(GLOBAL_COOKIES_FILENAME, "wb") as f:
#     chat=pickle.load(f)

chat = itchat.new_instance()
chat.auto_login(True,loginCallback=lc, exitCallback=ec)
user = chat.get_friends()
chat.search_friends(name='autolife')
print(chat.get_mps())
UserNames=[i['UserName'] for i in user if i['NickName'].find('龙漂') >=0 ]
# targetid=[i['NickName'] for i in user ]
# r=[i for i in targetid if i.find('Elly') >=0 ]
for UserName in UserNames:
    chat.send("Hello World!",toUserName=UserName)
#
# with open(GLOBAL_COOKIES_FILENAME, "wb") as f:
#     pickle.dump(chat, f)

sys.exit(0)

def saveCookie():
    with open(GLOBAL_COOKIES_FILENAME, "wb") as f:
        pickle.dump(chat, f)

def login():
    chat=itchat
    print(chat.dump_login_status())
    chat.auto_login(loginCallback=lc, exitCallback=ec)
    print(chat.dump_login_status())
    return isLogin()

def isLogin():
    return False

if isLogin():
    pass
else:
    login()

user = itchat.get_friends()
print(user)
sys.exit(1)
with open(GLOBAL_COOKIES_FILENAME, "rb") as f:
    cookies = pickle.load(f)

itchat.auto_login(loginCallback=lc, exitCallback=ec)
itchat.send("Hello World!")
# itchat.send(msg="Text Message", toUserName=None)

itchat.logout()  #强制退出登录
