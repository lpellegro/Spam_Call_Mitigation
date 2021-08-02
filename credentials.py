#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 16:39:35 2021

@author: lpellegr
"""

#for passwords and credentials customize the following file:
    
credentials = {'expe_cluster1':'expe1a.example.com', #FQDN of cluster1 primary peer
               'expe_cluster2':'expe2a.example.com', #FQDN of cluster2 primary peer; add more lines if other clusters are involved
               'url_cluster1':'https://expe1a.example.com', #URL for cluster1 (usually to the primary peer); the URL should include the port if different from 443 (see below)
               'url_cluster2':'https://expe2a.example.com:7443', #URL for cluster2 (includes port 7443 as admin HTTPS traffic uses this port)
               'expe1a.example.com':['admin', 'password1a'], #username and password for all peers in all clusters (see below)
               'expe1b.example.com':['admin', 'password1b'],
               'expe2a.example.com':['admin', 'password2a'], 
               'expe2b.example.com':['admin', 'password2b'], 
               'expe2c.example.com':['admin', 'password2c'],
               '192.0.2.201':'expe1a.example.com', #IP addresses for all peers in all clusters
               '192.0.2.202':'expe1b.example.com', 
               '203.0.113.201':'expe2a.example.com',
               '203.0.113.202':'expe2b.example.com',
               '203.0.113.203':'expe2c.example.com',
               'roomID':'<Your Webex room ID>', #Webex room ID to send and receive notifications
               'bearer':'<Your Webex Bearer>', #Webex Bot Bearer 
               'apikey':'<Your WhoisXMLAPI Key>', #API key to perform IP address lookup on https://www.whoisxmlapi.com
               'jailed_file':'<folder_path>/jailedIP.txt', #example: '/var/www/html/jailedIP.txt'
               'exempt_file':'<folder_path>/exemptions.txt', #example: '/var/www/html/exemptions.txt'
               'state_machine':'<folder_path>/card_status.csv', #example: '/var/www/html/card_status.csv'
               'activity_list_path':'<folder_path>'} #example: '/var/www/html/'

""" Example for a single peer cluser with user 'administrator' and password 'mysecret' that uses port 7443 as admin port

credentials = {'expe_cluster1':'expe.example.com', 
               'url_cluster1':'https://expe.example:7443',
               'expe.example.com':['administrator', 'mysecret'], 
               '192.0.2.301':'expe1a.example.com',
               'roomID':'abcdefghilmnopqrstuvz0123456789abcdefghilmnopqrstuvz0123456789abcdefghilmnopqrstuvz0123456789',
               'bearer':'MNBVCXZLKJGHGFDSAPOIUYTREWQMNBVCXZLKJGHGFDSAPOIUYTREWQMNBVCXZLKJGHGFDSAPOIUYTREWQ-09876-54321-012345678',
               'apikey':'ab_CDEFGHILMNOPQRST0123',
               'jailed_file':'/var/www/html/jailedIP.txt', 
               'exempt_file':'/var/www/html/exemptions.txt', 
               'state_machine':'/var/www/html/card_status.csv',
               'activity_list_path':'/var/www/html/'}

"""


