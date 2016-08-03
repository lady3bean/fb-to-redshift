#!/usr/bin/python
# -*- coding: utf-8 -*-

from settings import fb_version, fb_page_id, fb_long_token
import requests

def get_long_lived_token():
    user_access_token = 'add your user access token here'
    client_id = 'add your client id here'
    client_secret = 'add your client secret here'
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' %(client_id, client_secret, user_access_token)
    token = requests.get(url)
    return token.text[13:]

def get_page_access_token_from_user_token(long_user_access_token):
    url = base_url + '%s?fields=access_token&access_token=%s' %(fb_page_id, long_user_access_token)
    page_token = requests.get(url).json()   
    print(page_token['access_token'])
    
get_page_access_token_from_user_token(get_long_lived_token())