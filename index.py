# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 09:49:16 2021

@author: Hariom
"""

import requests
import senti_analysis as main_core

token = '1689180181:AAEKGUqUv2rZdm11JmWckTnRtxvThouqoI8'

api_url = "https://api.telegram.org/bot" + token
updates_url = api_url + "/getUpdates"


def get_url(temp):
    offset = temp
    url = updates_url + "?offset=" + str(offset) + "&timeout=100"
    return url


def send_msg(msg, ch_id):
    return requests.post(api_url + "/SendMessage" + "?chat_id=" + str(
        ch_id) + "&text=" + msg)


def last_update():
    resp = requests.get(updates_url)
    out = resp.json()['result']
    lst_updt = out[len(resp.json()['result']) - 1]
    return lst_updt['update_id'] + 1


ofst = last_update()


while True:
    response = requests.get(get_url(ofst))
    if len(response.json()['result']) > 0:
        msg = response.json()['result'][0]
        var = msg['message']['text']

        val = main_core.get_type(var)
        ret_msg = f"belonging sentence category is '{val}'"
        chat_id = msg['message']['chat']['id']
        send_msg(ret_msg, chat_id)
        ofst += 1

