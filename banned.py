#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 14:49:58 2021

@author: lpellegr
"""

#!/bin/sh
import requests
import json
import os
import csv
import urllib.parse
from datetime import datetime
from datetime import date
from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth
from expe import banunban
from cards_new import Card_3_buttons, Card_2_buttons
from credentials import credentials

def column(array, i):
    return [row[i] for row in array]

def local_peer (url, peer):
    parsed_url = urllib.parse.urlparse(url).netloc #take the LHS of the URL to identify the cluster in the response. returns https://expe1.example.com:7443 (with port)
    expe_list = parsed_url.split(':') #splits into a list: ['https://expe1.example.com', '7443']
    expe_ip = expe_list[0] #'https://expe1.example.com' this is the master
        
    if peer == '127.0.0.1':
       peer = expe_ip #equal to master if single peer
        
    if len(expe_list) == 1: #means no port needs to be added to the url
       peer_with_port = peer
 
    if len (expe_list) > 1:
       peer_with_port = peer + ':' + expe_list[1] #consider peer+port when doing ban/unban actions
    return peer, peer_with_port, parsed_url, expe_ip
    
def Expressway_cluster(url, username, secret, my_file, space, bearer, action_file,today, new_items):
   print ('NEW ITEMS AT THE BEGINNING OF THE SCRIPT:', new_items)
   day = str(today)
   #This functions prints a file with banned IPs from an Expressway cluster
   print("Query sent to:", url)
   try:
      response = requests.get(url, auth=HTTPBasicAuth(username, secret))
      storage=response.json()
      print ('Lenght of answer is:', len(storage))
      if len(storage)==0:
        print("JSON empty answer")
        return new_items
   except requests.exceptions.ConnectionError:
        print ('Connection error')
        return new_items
  
   card_identifier_list = []
   #read the jailedIP file and put the IPs in a list
   if not os.path.exists(my_file):
       open(my_file, 'w+')
   f=open(my_file, 'r+')
   all_the_lines = f.readlines()
   items = []
   #print("This is the txt banned IP file from the web:", all_the_lines)
   for i in all_the_lines: 
      items.append(i)
            
   #removes the /n from the list
   array_items = [x[:-1] for x in items] 
   print("This is the txt banned IP file from the web", array_items)
   
   if os.path.exists(action_file):
     with open(action_file, newline='') as a_f: 
      reader = csv.reader(a_f)
      action_list = list(reader)
     a_f.close()
   
   #append new items from JSON response to the list
   storindex=len(storage)
   print("This is a cluster of", storindex, "peers")
  
   old_len=len(array_items)
   print("last line is #", old_len)
   #new_items=[]
   new_peer_items=[]
   newitemflag=0   
   check_firewall_flag = 0
   #discover new IPs and append to the list
   for i in range(storindex):
       lenght=len(storage[i]['records'])
       print("Parsing peer", i)
       current_peer=storage[i]['peer']
       
       for j in range(lenght):
           if storage[i]['records'][j]['jail']=='sip-auth':
              ip=storage[i]['records'][j]['banned_address']
              if ip not in array_items:
                  print("New IP found:", ip)
                  #invoke a function to retrieve calling and called and real timestamps
                  calling, called, timestamp_day, timestamp_time, disconnect_cause, unban_flag, found = cdrcheck(url,username,secret,ip,'/api/management/status/call/call')
                  #print (calling, called, timestamp_day, timestamp_time, disconnect_cause)
                  if found == 1 and unban_flag == 0:
                     print('IP jailed')
                     array_items.append(ip) 
                  #print('IP automatically removed from the list')
                  new_items.append([ip, calling, called, timestamp_day, timestamp_time, current_peer, disconnect_cause, 0, day])
                  print ('NEW ITEMS LIST IS: ', new_items)
                  newitemflag=1
              else:
                  peer, peer_with_port, parsed_url, expe_ip = local_peer (url, current_peer)
                  card_id = ip + ':' + peer
                  card_identifier_list = column (action_list, 0)
                  if card_id not in card_identifier_list:
                     calling, called, timestamp_day, timestamp_time, disconnect_cause, unban_flag, found = cdrcheck(url,username,secret,ip,'/api/management/status/call/call')
                     print ('New IP items list is: ', new_items)
                     new_ip_items = column (new_items, 0)
                     print ('New IP items are: ', new_ip_items)
                     if ip not in new_ip_items:
                       print ('IP: ' + ip + ' IN GLOBAL LIST BUT RECEIVED ON PEER: CHECK FW')
                       check_firewall_flag = 1 #check firewall alert should be sent only if the IP is in the old list (array_items), not if it is has just been found (in this case is in new_items)
                     else:
                       check_firewall_flag = 0
                       print ('IP: ' + ip + ' RECEIVED ON PEER CONCURRENTLY WITH ANOTHER. DO NOT NEED TO CHECK THE FW')
                     new_peer_items.append([ip, calling, called, timestamp_day, timestamp_time, peer, disconnect_cause, check_firewall_flag, day])
                  else:
                     new_ip_items = column (new_items, 0)
                     if ip in new_ip_items:
                       calling, called, timestamp_day, timestamp_time, disconnect_cause, unban_flag, found = cdrcheck(url,username,secret,ip,'/api/management/status/call/call')
                       new_peer_items.append([ip, calling, called, timestamp_day, timestamp_time, peer, disconnect_cause, 0, ''])
                     
   if newitemflag==0:
      print("No new IP found")
   #newitemflag=1 means new IP found; get WHOIS info and print on a file
   if newitemflag==1:
      f= open(my_file, "w+")
      l=len(array_items) 
      for i in range(l):
         f.write(array_items[i] + "\n")
      f.close()
      send_card(new_items, url, action_file, today, space, bearer, 0, unban_flag, found) # 0 means that a new IP has been found, so the cards will be sent for every new IP
   
   if new_peer_items != []:
      print(new_peer_items)
      send_card (new_peer_items, url, action_file, today, space, bearer, 1, unban_flag, found) #1 means that a new IP peer has been found, so the card will be sent for that IP also
   print ('New items from banned whike in banned: ', new_items)
   return new_items

def send_card (any_list, url, action_file, today, space, bearer, new_peer, unban_flag, found):
      day = str (today)
      n=len(any_list)
      for index in range(n):
        ip=any_list[index][0]
        peer=any_list[index][5]
        calling_id=any_list[index][1]
        if calling_id=='':
           calling_id='Unknown'
        called_id=any_list[index][2]
        if called_id=='':
           called_id='Unknown'
        if calling_id == 'Unknown' and called_id == 'Unknown':
           calling_id = 'No call activities'
           called_id = 'No call activities'
        peer, peer_with_port, parsed_url, expe_ip = local_peer (url, peer)
        disconnect_cause = any_list[index][6]
        check_firewall_flag = any_list[index][7]
        print ('ANY LIST IS: ', any_list)
        day_in_list = any_list[index][8]
        if day_in_list != '':
           day = str(day_in_list)
        card_identifier = ip + ':' + peer
        action_list = []
        banned_counter = 0
        unbanned_counter = 0
        
        if os.path.exists(action_file):
           with open(action_file, newline='') as a_f: 
               reader = csv.reader(a_f)
               action_list = list(reader)
               #rint(action_list)
               for i, v in enumerate(action_list):
                 if v[0] == card_identifier:
                   post_id = action_list [i][1]
                   delete_url = 'https://webexapis.com/v1/messages/' + post_id
                   webex_delete = requests.delete (delete_url, headers={'Authorization': 'Bearer ' + bearer})
                   banned_counter = int(action_list [i][3])
                   unbanned_counter = int(action_list [i][4])
                   day = str(action_list [i][8])
                   action_list.remove (action_list[i])
        print ('Found flag is: ', found, ' Unban flag is: ', unban_flag)
        if found == 0 or unban_flag == True: #in this case unban
           flag_exempt = False
           flag_remove_exemption = True

           #case of cluster made by 1 peer, with standard or dedicated port
  
           print('Peer to connect to with port is: ', peer_with_port)
           
           user=credentials[expe_ip][0]
           secret=credentials[expe_ip][1]
           print('username: ', user, 'password: ', secret)
           error = banunban(peer_with_port, user, secret, ip, 'unban', space)
           if error == '':
              button_1 = 'Ban'
              button_1_action = 'ban'
              button_2 = 'Exempt'
              button_2_action = 'exempt'
              values_text1="**New IP automatically unbanned**:  " + ip + "\r\n" + "Calling: " + calling_id + "Called:  " + called_id + "\r\n"
              if unbanned_counter > 0:
                 unbanned_counter +=1
                 title = 'AUTOMATICALLY UNBANNED'
                 history = 'First seen ' + day + '. Automatically unbanned ' + str(unbanned_counter) + ' times'
              else: 
                 title = 'NEW IP AUTOMATICALLY UNBANNED'
                 unbanned_counter = 1
                 history = ''
              imageurl = 'https://upload.wikimedia.org/wikipedia/commons/7/75/Prison_door_icon.png'
              card = Card_3_buttons(title, ip, imageurl, calling_id, called_id, parsed_url, peer, button_1, button_1_action, button_2, button_2_action, history, day)
              card_status = 'unbanned'
              values_text1="**New IP unbanned**:  " + ip + "\r\n" + "Calling: " + calling_id + "Called:  " + called_id + "\r\n"
        else:
         if banned_counter > 0:
            banned_counter +=1
           
            title = 'AUTOMATICALLY BANNED'
            history = 'First seen ' + day + '. Automatically banned ' + str(banned_counter) + ' times'
         else:
            title = 'NEW IP AUTOMATICALLY BANNED'
            banned_counter = 1
            if new_peer == 1:
              if check_firewall_flag == 1:
                 history = 'Check your firewall. This IP was already present in the global list'
              else:
                 history = ''
            else:
               history = ''
         imageurl = 'https://www.flaticon.com/premium-icon/icons/svg/2710/2710040.svg'
         button_1 = 'Unban'
         button_1_action = 'unban'
         card = Card_2_buttons(title, ip, imageurl, calling_id, called_id, parsed_url, peer, button_1, button_1_action, history, day)
         card_status = 'banned'
         values_text1="**New IP banned**:  " + ip + "\r\n" + "Calling: " + calling_id + "Called:  " + called_id + "\r\n"
        
        values_string=values_text1 #+ values_text2 + values_text3
        #print(values_string, type(values_string))
        

        print ('This card has parsed url =', parsed_url)
        print ('This card has peer =', peer)
        webex_url="https://webexapis.com/v1/messages"
        headers = {
  'Authorization': 'Bearer ' + bearer,
  'Content-Type': 'application/json'
          }
        payload = json.dumps({
"roomId": space,
  "text": values_string,
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": card

    }
  ]
})
        response = requests.request("POST", webex_url, headers=headers, data=payload)
        resp = response.json()
        message_id=resp['id']
                
        action_list.append([card_identifier, message_id, card_status, banned_counter, unbanned_counter, calling_id, called_id, parsed_url, day])
        with open(action_file, 'w+', newline='') as a_f:
          write = csv.writer(a_f) 
          write.writerows(action_list)              
        #print("RISPOSTA DEL POST", response)
        #print("CARD POST RESPONSE IS", response.text)


def cdrcheck(url, username, secret, newip, cdrurl):
    host_url=urlparse(url).netloc
    #query='/api/management/status/call/call'
    new_url='https://'+host_url+cdrurl
    response = requests.get(new_url, auth=HTTPBasicAuth(username, secret))
    print("CDR query sent to:", new_url)
    print(type(response))
    r=response.json()
    #print ('La risposta è', r)
    #print('La lunghezza della risposta è:', len(r))

    source_alias='Unknown'
    destination_alias='Unknown'
    day='Unknown'
    time='Unknown'
    disconnect_reason = 'Unknown'
    if len(r)==0:   
       print("JSON empty answer")
       return source_alias, destination_alias, day, time, disconnect_reason
    peers=len(r)
    found=0
    unban_flag = False
    for peer in range(peers):
        calls=r[peer]['num_recs']
        #print("Chiamate", calls)
        call_record=r[peer]['records']
        #print("call_record", call_record)
        for call in range(calls):
            #print ('numero chiamata', call)
            call_details=call_record[call]['details'] #string just works fine
            if newip in call_details:
               if found == 0:
                  found=1
                  source_alias=call_record[call]['source_alias']
                  destination_alias=call_record[call]['destination_alias']
                  timestamp=call_record[call]['start_time'][:-7]
                  timestamp_list=timestamp.split(" ")
                  day=timestamp_list[0]
                  time=timestamp_list[1]
                  disconnect_reason=call_record[call]['disconnect_reason']
                  if disconnect_reason != '403 Forbidden' and disconnect_reason != 'Unknown':
                    unban_flag = True 
                  #return source_alias, destination_alias, day, time, disconnect_reason
               else: 
                  if disconnect_reason != '403 Forbidden' and disconnect_reason != 'Unknown':
                    unban_flag = True
            
    return source_alias, destination_alias, day, time, disconnect_reason, unban_flag, found
               



