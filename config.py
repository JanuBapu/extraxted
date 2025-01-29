#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) ACE 

import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6478481960:AAFsRb8UGX3VCA_b3_mIUn_Biz8TZ-tvQZM")
    API_ID = int(os.environ.get("API_ID", "22594398"))
    API_HASH = os.environ.get("API_HASH", "3a2408d97d6a222d87766dac2da302df")
    AUTH_USERS = "5357048091"

