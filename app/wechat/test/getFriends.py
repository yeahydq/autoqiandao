# -*- coding: UTF-8 -*-
import itchat
import re

itchat.login()

user = itchat.get_friends()

i = str(user[:1])
print(i)
info = i[8:-2]
print(info)

name = str(re.findall(r"'NickName': '(.+?)'", info))[2:-2]
sign = str(re.findall(r"'Signature': '(.+?)'", info))[2:-2]
sex = str(re.findall(r"'Sex': (.+?),", info))[2:-2]
uin = str(re.findall(r"'Uin': (.+?),", info))[2:-2]
print(name)
print(sign)
print(sex)
print(uin)
