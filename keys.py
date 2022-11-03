#!/usr/bin/env python
# -*- coding: utf-8 -*-

# twitter 개발자 등록하여 키값 가져와서 작성하면 됨.
keys = dict(
API_KEY=
API_SECRET_KEY=
BEARER_TOKEN=
ACCESS_TOKEN=
ACCESS_TOKEN_SECRET=
)

user_name = #@ 뺀 id 값 입력.

FOLLOW_ONLY = 1
FOLLOWING_ONLY = 2
EACH_FOLLOW = FOLLOW_ONLY + FOLLOWING_ONLY


DIR_PATH = "/var/log/twit"
DIFF_FILE_PATH = "%s/%s" %(DIR_PATH, "friends-diff.log")
