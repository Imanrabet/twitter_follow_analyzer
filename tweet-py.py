#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# depend on tweepy 4.x (3.x do not work)
import tweepy, time, sys, datetime
import time
from datetime import date, timedelta

from keys import *
# github에 올리기 위해, keys.py 파일을 따로 만들어서 관리함.

def get_user_id(client, user_name):
    user, err, include, meta = client.get_user(username=user_name)
    uid = 0
    uid = user.id
    return uid

def list_up_followers(client, uid, today_user_d, twitter_id_list):
    user_list, err, include, meta = client.get_users_followers(id=int(uid), max_results=1000)
    for user in user_list:
        if (user.username in today_user_d) == False:
            today_user_d[user.username] = FOLLOW_ONLY
        if (user.username in twitter_id_list) == False:
            twitter_id_list[user.username] = user.id
    print("follower count : %d" % meta['result_count'])

def list_up_followings(client, uid, today_user_d, twitter_id_list):
    user_list, err, include, meta = client.get_users_following(id=int(uid), max_results=1000)
    for user in user_list:
        if (user.username in today_user_d) == False:
            today_user_d[user.username] = FOLLOWING_ONLY
        if (user.username in twitter_id_list) == False:
            twitter_id_list[user.username] = user.id
        today_user_d[user.username] = today_user_d[user.username] + FOLLOWING_ONLY
    print("following count : %d" % meta['result_count'])

def save_today_data_to_file(today_str, twitter_id_list, today_user_d):
    """
    # 기록용 오늘의 로그 파일 생성.
    # 파일명 : twitter-연도월일.log 예) twitter-20221103.log
    # 기록 내용 : username,id,status
    """
    file_path = "%s/friends-%s.log" % (DIR_PATH, today_str)
    with open(file_path, 'w') as f :
        for user in today_user_d:
            f.write("%s,%d,%d\n" %(user, twitter_id_list[user],today_user_d[user]))

def save_today_n_yestd_diff_to_file(yesterday_str, today_user_d, mod_d, add_d, del_d):
    """
    # 어제의 기록을 읽어와서 오늘의 내용과 비교.
    # 저장 파일명 : twitter-연도월일.diff.log 예) twitter-20221103.diff.log
    # 기록 내용 :
    #[deleted]
    #EACH/Following/Follower list
    #[append]
    #EACH/Following/Follower list
    """
    yesterday_d = {}
    yesterday_file_path = "%s/friends-%s.log" % (DIR_PATH, yesterday_str)
    with open(yesterday_file_path, 'r') as f :
        while True:
            line = f.readline()
            if not line: break
            split_strings = line.split(",")
            user = split_strings[0].strip()
            uid = int(split_strings[1].strip())
            status = int(split_strings[2].strip())
            yesterday_d[user] = status
            #print ("%s,%d,%d\n" % (user, uid, status))
            if user in today_user_d:
                # 있는데 값이 다를 경우 > 상태가 변경됨. modify.
                if today_user_d[user] != status:
                    mod_d[user] = status
                    print("status err")
                    print ("MOD %s,%d,%d\n" % (user, uid, status))
    			#print("exist")
            else:
                # 어제거가 오늘거에 없는 경우. > 추가. add
                add_d[user] = status
                print ("ADD %s,%d,%d\n" % (user, uid, status))
        # 오늘거가 어제거에 없는 경우. > 제거. del
        for user in today_user_d:
            if (user in yesterday_d) == False:
                del_d[user] = status
                print ("DEL %s,%d,%d\n" % (user, uid, status))


def write_differents(today_str, mod_d add_d, del_d):
    with open(DIFF_FILE_PATH, 'a') as f:
        f.write("%s twitter f/f log\n" % today_str)
        f.write("[mod_d] : %d\n" % len(mod_d))
        for user in mod_d:
            f.write("%s,%d\n" %(user, mod_d[user]))

        f.write("[del_d] : %d\n" % len(del_d))
        for user in del_d:
            f.write("%s,%d\n" %(user, del_d[user]))

        f.write("[add_d] : %d\n" % len(add_d))
        for user in add_d:
            f.write("%s,%d\n" %(user, add_d[user]))

def main():
    auth = tweepy.OAuthHandler(keys['API_KEY'], keys['API_SECRET_KEY'])
    auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    client = tweepy.Client(keys['BEARER_TOKEN'])

    uid = get_user_id(username=user_name)
    if uid == 0:
        print("invalid uid")
        return

    today_user_d = {}
    twitter_id_list = {}

    list_up_followers(client, uid, today_user_d, twitter_id_list)
    list_up_followings(client, uid, today_user_d, twitter_id_list)

    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    save_today_data_to_file(today_str, twitter_id_list, today_user_d)

    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    save_today_n_yestd_diff_to_file(yesterday_str, today_user_d, mod_d, add_d, del_d)

    write_differents(today_str, mod_d add_d, del_d)

if __name__ == '__main__':
    main()

