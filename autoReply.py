import itchat
import requests
from itchat.content import *

# 注册图灵账号，创建图灵机器人或获取的key
def AI_Talk(msg):
    response = requests.post("http://www.tuling123.com/openapi/api",
    data={"key":"4b48e16bb9c84de5aaac80286ad45cb3", "info": msg, "userid": "123456" })
    response = response.json()
    answer=response['text']
    return answer

@itchat.msg_register(TEXT,PICTURE)
def text_reply(msg):
    print ("receive text msg is: ", msg)
    return AI_Talk(msg['Text'])

@itchat.msg_register(PICTURE)
def simple_reply(msg):
    print ("receive simple msg is: ", msg)
    userinfo = msg['User']
    text = "姓名：{nickname} \n" \
           "地区：{province} \n" \
           "性别：{sex} \n" \
           "签名：{signature}".format(nickname=userinfo['NickName'],
                                   province=(userinfo['Province']+" "+userinfo["City"]),
                                   sex=("男" if userinfo['Sex']==1 else "女"),
                                   signature=userinfo['Signature'])
    return "你的信息是：\n"+ text + "\n" + AI_Talk(msg['Text'])

@itchat.msg_register
def general_reply(msg):
    print ("receive general msg is: ", msg)
    return 'I received a %s' % msg['Type']

def getFriends():
    itchat.auto_login()
    friends = itchat.get_friends(update=True)
    return friends


def my_friends_sex(friends):
    # 创建一个字典用于存放好友性别信息
    friends_sex = dict()
    # 定义好友性别信息字典的key，分别为男性，女性，其他
    male = "男性"
    female = "女性"
    other = "其他"

    # 遍历列表中每一个好友的信息，
    for i in friends[1:]:
        sex = i["Sex"]
        if sex == 1:
            # 字典操作，找到key并为其的值加1
            friends_sex[male] = friends_sex.get(male, 0) + 1
        elif sex == 2:
            friends_sex[female] = friends_sex.get(female, 0) + 1
        elif sex == 0:
            friends_sex[other] = friends_sex.get(other, 0) + 1
    # 打印好友性别信息的字典
    # print (friends_sex)
    # 好友总数，从第二个开始是因为第一个好友是自己
    totle = len(friends[1:])

    proportion = [float(friends_sex[male]) / totle * 100, float(friends_sex[female]) / totle * 100,
                  float(friends_sex[other]) / totle * 100]
    print(
        "男性好友：%.2f%% " % (proportion[0]) + '\n' +
        "女性好友：%.2f%% " % (proportion[1]) + '\n' +
        "其他：%.2f%% " % (proportion[2])
    )
    return friends_sex


# friends = getFriends()
# print (my_friends_sex(friends))


itchat.auto_login(hotReload=True)
itchat.run()
itchat.dump_login_status()
