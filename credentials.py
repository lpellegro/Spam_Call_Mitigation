#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 16:39:35 2021

@author: lpellegr
"""

#For passwords and credentials customize the following file. Following a template config for 2 different clusters, one with 2 Expressway-E and another with 3.
#Item order is not relevant
#CHANGE THIS:
#----------------------------------------------------------------------------------

credentials = {#EXPRESSWAY SECTION
               #Cluster 1
               'expe_cluster1':'expe1a.example.com', #FQDN of cluster1 primary peer
               'url_cluster1':'https://expe1a.example.com', #URL for cluster1 (usually to the primary peer); the URL should include the port if different from 443 
               'expe1a.example.com':['admin', 'password1a'], #username and password for all peers in all clusters 
               'expe1b.example.com':['admin', 'password1b'],
               '192.0.2.201':'expe1a.example.com', #IP addresses for all peers in all clusters
               '192.0.2.202':'expe1b.example.com', 
               #Cluster 2 (remove if not present)
               'expe_cluster2':'expe2a.example.com', #FQDN of cluster2 primary peer; add more lines if more clusters are involved 
               'url_cluster2':'https://expe2a.example.com:7443', #URL for cluster2 (includes port 7443 as admin HTTPS traffic uses this port)
               'expe2a.example.com':['admin', 'password2a'], 
               'expe2b.example.com':['admin', 'password2b'], 
               'expe2c.example.com':['admin', 'password2c'],
               '203.0.113.201':'expe2a.example.com',
               '203.0.113.202':'expe2b.example.com',
               '203.0.113.203':'expe2c.example.com',
               #Add more clusters if required
               #......
               #CLOUD SECTION
               'roomID':'<Your Webex room ID>', #Webex room ID to send and receive notifications
               'bearer':'<Your Webex Bearer>', #Webex Bot Bearer 
               'apikey':'<Your WhoisXMLAPI Key>', #API key to perform IP address lookup on https://www.whoisxmlapi.com
               #LOCAL FILE SECTION
               'jailed_file':'<folder_path>/jailedIP.txt', #example: '/var/www/html/jailedIP.txt'
               'exempt_file':'<folder_path>/exemptions.txt', #example: '/var/www/html/exemptions.txt'
               'state_machine':'<folder_path>/card_status.csv', #example: '/var/www/html/card_status.csv'
               'activity_list_path':'<folder_path>'} #example: '/var/www/html/'
#--------------------------------------------------------------------------------------

#EXAMPLES

""" Single peer cluster with user 'administrator' and password 'mysecret' that uses port 7443 as admin port

credentials = {'expe_cluster1':'expe.example.com', 
               'url_cluster1':'https://expe.example.com:7443',
               'expe.example.com':['administrator', 'mysecret'], 
               '192.0.2.301':'expe.example.com',
               'roomID':'abcdefghilmnopqrstuvz0123456789abcdefghilmnopqrstuvz0123456789abcdefghilmnopqrstuvz0123456789',
               'bearer':'MNBVCXZLKJGHGFDSAPOIUYTREWQMNBVCXZLKJGHGFDSAPOIUYTREWQMNBVCXZLKJGHGFDSAPOIUYTREWQ-09876-54321-012345678',
               'apikey':'ab_CDEFGHILMNOPQRST0123',
               'jailed_file':'/var/www/html/jailedIP.txt', 
               'exempt_file':'/var/www/html/exemptions.txt', 
               'state_machine':'/var/www/html/card_status.csv',
               'activity_list_path':'/var/www/html/'}

Two clusters, 2 and 3 peers, one with standard admin port and another using 7443. Same username and passwords.

credentials = {'expe_cluster1':'expe1a.example.com', 
               'url_cluster1':'https://expe1a.example.com',
               'expe1a.example.com':['admin', 'password1a'], 
               'expe1b.example.com':['admin', 'password1b'],  
               '192.0.2.201':'expe1a.example.com', 
               '192.0.2.202':'expe1b.example.com', 

               'expe_cluster2':'expe2a.example.com', 
               'url_cluster2':'https://expe2a.example.com:7443', 
               'expe2a.example.com':['admin', 'password2a'], 
               'expe2b.example.com':['admin', 'password2b'], 
               'expe2c.example.com':['admin', 'password2c'],
               '203.0.113.201':'expe2a.example.com',
               '203.0.113.202':'expe2b.example.com',
               '203.0.113.203':'expe2c.example.com',

               'roomID':'abcdefghilmnopqrstuvz0123456789abcdefghilmnopqrstuvz0123456789abcdefghilmnopqrstuvz0123456789', 
               'bearer':'MNBVCXZLKJGHGFDSAPOIUYTREWQMNBVCXZLKJGHGFDSAPOIUYTREWQMNBVCXZLKJGHGFDSAPOIUYTREWQ-09876-54321-012345678', 
               'apikey':'ab_CDEFGHILMNOPQRST0123', 

               'jailed_file':'/var/www/html/jailedIP.txt', 
               'exempt_file':'/var/www/html/exemptions.txt', 
               'state_machine':'/var/www/html/card_status.csv', 
               'activity_list_path':'/var/www/html'} 
"""


