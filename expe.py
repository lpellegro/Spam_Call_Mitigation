import logging
import json
import requests
from requests.auth import HTTPBasicAuth
import paramiko, time
from datetime import datetime
from datetime import date
import socket
import os
from paramiko.client import SSHClient, AutoAddPolicy
from webex_bot.cards.echo_card import ECHO_CARD_CONTENT
from webex_bot.formatting import quote_info
from webex_bot.models.command import Command
import csv
from cards_new import Card_3_buttons, Card_2_buttons
from credentials import credentials

log = logging.getLogger(__name__)

def terminal(target, user, password, action, ip, space):
   # Connect to terminal to exempt an ip
  status="Unknown error"
  try:
   client = SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   print('Connecting to terminal...', target, 'username: ', user, 'password: ', password)
   client.connect(target, username=user, password=password)

   remote_conn=client.invoke_shell()
   time.sleep(2)
   output=remote_conn.recv(1000)
   # Run a command (execute PHP interpreter)


   remote_conn.send('\n') # I only want output from this command.
   time.sleep(2)
   output=remote_conn.recv(1000)
   print('action is', action)
   suffix=''
   if action=='exempt' or action=='Exempt':
     print('should be exempted', action)
     suffix='Add'
     msg_to_space='exempted'
   else:
     if action=='unexempt' or action=='Unexempt':
       print('should be removed', action)
       suffix='Delete'
       msg_to_space='exemption removed'
     else:
       status='error'
       return status
   print('Suffix is:', suffix)
   message='xcommand Fail2banExemption'+suffix+' '+ip+ '/32 Jail: "sip-auth"\n'
   print(message)
   remote_conn.send(message)
   # Getting output I want.
   time.sleep(2)
   #if remote_conn.recv_ready():
   output = remote_conn.recv(8000)
   #print('Output is:', output)
   #print (type(output))
   result=str(output)
   print('Result of operation is:', result)
   print('Result is of type:',type(result))
   #result_list=result.split()
   #print(result_list)
   found=0

   #print(findresult)
   if 'status=OK' in result:
       print('success')
       found=1
       status='success'
       #return status

   if 'already exists' in result:
       found=1
       status='already exempted'
       print('Record already exists')
       #return status

   if found==0:
      print ('Error: got unexpected result')
      status='FAILED '
   expe=target.split(":", 1)[0]

  except paramiko.AuthenticationException:
     print("Authentication failed, please verify your credentials: %s")
  except paramiko.SSHException as sshException:
     print("Unable to establish SSH connection: %s" % sshException)
  except paramiko.BadHostKeyException as badHostKeyException:
     print("Unable to verify server's host key: %s" % badHostKeyException)
  except socket.timeout as error:
     print("Timeout error")
  finally:
   # Close the client itself
   client.close()
   return status
  
def banunban(target, user, secret, ip, action, space):
    if action=='unban':
       apicommand='unbanip'
       apiaction='unban'
    if action=='ban':
       apicommand='banip'
       apiaction='ban'
    data={'command':apicommand, 'jail':'sip-auth', 'argument': ip}
    #if target includes an IP address instead of hostname the REST API will generate an error. The following is to convert the IP into FQDN. Remember to append the port to the IP, i.e. 192.0.2.1:902
    #if target in credentials:
       #dnsname = credentials[target]
       #target = str(dnsname)
    url='https://'+ target +'/api/management/commands/fail2ban'
    print ('sending API request to: ', url)
    error = ''
    try:
       response=requests.post(url, data, auth=HTTPBasicAuth(user, secret))
       r=response.json()
       print(apicommand + ' response is: ', r)
       #check the status of the request
       id=r[0]['uuid']
       print(id)
       new_url='https://' + target + '/api/management/commands/fail2ban' + '/uuid/' + id
       time.sleep(2)
       r_status=requests.get(new_url, auth=HTTPBasicAuth(user, secret)) 
       status=r_status.json()
       print(apicommand + ' status is: ', status)
       result=status[0]['records'][0]['command_state']
       error=status[0]['records'][0]['command_error']
       print('result is: ', result)
       if error != '':
         print('error is: ', error)
       return error
       expe=target.split(":", 1)[0]

    except:
       error = 'Error'
       return error
       pass

def updatefiles(ip_address, execution, exemption_list, jailed_list):
       #creates exemption file if doesn't exist. If exists, includes the items into a list
       
       if not os.path.exists(exemption_list):
          open(exemption_list, 'w+')
       e=open(exemption_list, 'r+')
       e_all_the_lines = e.readlines()
       #print("This is the txt banned IP file from the web:", all_the_lines)
       e_items = []
       for i in e_all_the_lines: 
          e_items.append(i)
       e.close()
       
       #creates jailed file if doesn't exist. If exists, includes the items into a list
       if not os.path.exists(jailed_list):
          open(jailed_list, 'w+')
       j=open(jailed_list, 'r+')
       j_all_the_lines = j.readlines()
       j_items = []
       for i in j_all_the_lines: 
         j_items.append(i)
       j.close()  
       
       #removes the /n from the exemption and jailed list
       e_array_items = [x[:-1] for x in e_items] 
       j_array_items = [x[:-1] for x in j_items]
       
       print("This is the exempted list: ", e_array_items)
       print("This is the banned list: ", j_array_items)
       
       if execution == 'ban':
          if ip_address not in j_array_items:
             j_array_items.append(ip_address)
           
       if execution == 'unban':
          if ip_address in j_array_items:
             j_array_items.remove(ip_address) 
         
       if execution == 'exempt':
          if ip_address not in e_array_items:
             e_array_items.append(ip_address)
       
       if execution == 'unexempt':
          if ip_address in e_array_items:
             e_array_items.remove(ip_address)
       
       e= open(exemption_list, "w+")
       l=len(e_array_items) 
       for i in range(l):
         e.write(e_array_items[i] + "\n")
       e.close()

       j= open(jailed_list, "w+")
       l=len(j_array_items) 
       for i in range(l):
         j.write(j_array_items[i] + "\n")
       j.close()    
    

class ExpeCommand(Command):

    def __init__(self):
        super().__init__(
            command_keyword="callback___exempt",
            help_message="Exempt an IP",
            card=ECHO_CARD_CONTENT)

    def execute(self, message, attachment_actions):
        """
        If you want to respond to a submit operation on the card, you
        would write code here!

        You can return text string here or even another card (Response).

        This sample command function simply echos back the sent message.

        :param message: message with command already stripped
        :param attachment_actions: attachment_actions object
        :return: a string or Response object. Use Response if you want to return another card.
        """
        #exempt on Expressway
        
        room_id = credentials['roomID']
        jailed_file = credentials['jailed_file']
        exempt_file = credentials['exempt_file']
        state_machine = credentials['state_machine']
        bearer = credentials['bearer']
        print ('ATTACHMENT ACTIONS: ', attachment_actions, ' TYPE: ', type(attachment_actions))
        jsonstr = json.dumps (attachment_actions.__dict__)
        print('TYPE JSONSTR AND JSONSTR ARE: ', type(jsonstr), jsonstr)
        json_actions = json.loads(jsonstr)
        ip = json_actions['_json_data']['inputs']['IP']
        action = json_actions['_json_data']['inputs']['action']
        expe = json_actions['_json_data']['inputs']['expe']
        peer = json_actions['_json_data']['inputs']['peer']
        day = json_actions['_json_data']['inputs']['time']
        print('IP IS: ', ip, ' ACTION IS: ', action, ' EXPE IS: ', expe, 'PEER IS: ', peer) 
        
        expe_list = expe.split(':')
 
        expe_ip = expe_list[0]
        if peer == '127.0.0.1':
           peer = expe_ip
        
        if len(expe_list) == 1: #use of standard port for https (443)
           peer_with_port = peer
 
        if len (expe_list) > 1:
           peer_with_port = peer + ':' + expe_list[1]
        #case of cluster made by 1 peer, with standard or dedicated port
        
        user=credentials[expe_ip][0]
        secret=credentials[expe_ip][1]
        
        print('Peer to connect to with port is: ', peer_with_port)
        if action == 'ban' or action == 'unban':
           error = banunban(peer_with_port, user, secret, ip, action, room_id)
        if action == 'exempt' or action == 'unexempt':
           done=terminal(expe_ip, user, secret, action, ip, room_id)
           print(done)
           if 'error' in done or done == 'FAILED':
              error = 'error'
              fqdnexpe = expe.split(":", 1)[0] #split the fqdn in 2 pieces and removes the :port
              values={'roomId': room_id, 'markdown':'Generic error or unable to connect to '+fqdnexpe}
           else:
              error = ''
        if error == '':
          updatefiles(ip, action, exempt_file, jailed_file)
          state_index = ip + ':' + peer
          banned_counter = 0
          unbanned_counter = 0
          with open(state_machine, newline='') as a_f:
            reader = csv.reader(a_f)
            action_list = list(reader)
            print(action_list)
            for i, v in enumerate(action_list):
              if v[0] == state_index:
                 post_id = action_list [i][1]
                 banned_counter = int(action_list [i][3])
                 unbanned_counter = int(action_list [i][4])
                 calling_id = action_list [i][5]
                 called_id = action_list [i][6]
                 parsed_url = action_list[i][7]
                 first_seen_timer = action_list[i][8]
                 #status_id = action_list [i][2]
                 print ('post id is: ', post_id)
                 #print ('status id is: ', status_id)
            delete_url = 'https://webexapis.com/v1/messages/' + post_id
            webex_delete = requests.delete (delete_url, headers={'Authorization': 'Bearer ' + bearer})
            action_list.remove (action_list[i])
          if banned_counter > 0:
             history_part_1 = '. Automatically banned ' + str(banned_counter) + ' times.'
          else:
             history_part_1 = ''
          if unbanned_counter > 0:
             history_part_2 = ' Automatically unbanned ' + str(unbanned_counter) + ' times.'
          else:
             history_part_2 = ''
          history = 'First seen ' + day + history_part_1 + history_part_2
          if action == 'ban':       
             button_1 = 'Unban'
             button_1_action = 'unban'
             title = 'IP BANNED'
             imageurl = 'https://www.flaticon.com/premium-icon/icons/svg/2710/2710040.svg'
             values_string = "**IP BANNED**:  " + ip + "\r\n" + "Calling: " + calling_id + "Called:  " + called_id + "\r\n"
             card = Card_2_buttons(title, ip, imageurl, calling_id, called_id, parsed_url, peer, button_1, button_1_action, history, day)
             card_status = 'banned'
          
          if action == 'unban':       
             button_1 = 'Ban'
             button_1_action = 'ban'
             button_2 = 'Exempt'
             button_2_action = 'exempt'
             title = 'IP UNBANNED'
             imageurl = 'https://upload.wikimedia.org/wikipedia/commons/7/75/Prison_door_icon.png'
             values_string = "**IP UNBANNED**:  " + ip + "\r\n" + "Calling: " + calling_id + "Called:  " + called_id + "\r\n"
             card = Card_3_buttons(title, ip, imageurl, calling_id, called_id, parsed_url, peer, button_1, button_1_action, button_2, button_2_action, history, day)
             card_status = 'unbanned'
          
          if action == 'exempt':
             button_1 = 'Remove Exemption'
             button_1_action = 'unexempt'
             title = 'IP EXEMPTED'
             imageurl = 'https://previews.123rf.com/images/webstocker/webstocker1610/webstocker161000002/63871577-red-carpet-entrance-icon.jpg'
             values_string = "**IP EXEMPTED**:  " + ip + "\r\n" + "Calling: " + calling_id + "Called:  " + called_id + "\r\n"
             card = Card_2_buttons(title, ip, imageurl, calling_id, called_id, parsed_url, peer, button_1, button_1_action, history, day)
             card_status = 'exempted'
             
          if action == 'unexempt':
             button_1 = 'Ban'
             button_1_action = 'ban'
             button_2 = 'Exempt'
             button_2_action = 'exempt'
             title = 'IP EXEMPTION REMOVED - UNBANNED'
             imageurl = 'https://www.shareicon.net/data/128x128/2015/09/15/641035_man_512x512.png'
             values_string = "**IP UNEXEMPTED**:  " + ip + "\r\n" + "Calling: " + calling_id + "Called:  " + called_id + "\r\n"
             card = Card_3_buttons(title, ip, imageurl, calling_id, called_id, parsed_url, peer, button_1, button_1_action, button_2, button_2_action, history, day)
             card_status = 'unexempted'
             
          webex_url="https://webexapis.com/v1/messages"
          headers = {
  'Authorization': 'Bearer ' + bearer,
  'Content-Type': 'application/json'
          }
          payload=payload = json.dumps({
      "roomId": room_id,
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
          print (resp)
          message_id=resp['id']
        
        
          card_identifier = ip + ':' + peer
          action_list.append([card_identifier, message_id, card_status, banned_counter, unbanned_counter, calling_id, called_id, parsed_url, first_seen_timer])
          with open(state_machine, 'w+', newline='') as a_f:
            write = csv.writer(a_f) 
            write.writerows(action_list)              
  
             
             
          
            
         
          
              
        
        
        
   
        #return quote_info(attachment_actions.inputs.get("Got the exempt message"))
        #return quote_info(attacihment_actions.inputs.get("message_typed"))
                  
