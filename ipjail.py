from datetime import datetime
from datetime import date
from credentials import credentials
from banned import Expressway_cluster

print("START LINE --------------------------------------------------------")
now=datetime.now()
current_time = now.strftime("%H:%M:%S")
today=date.today()
print("Script run at", current_time, today)
roomID = credentials['roomID']

bearer = credentials['bearer']
jailed_file = credentials['jailed_file']
exempt_file = credentials['exempt_file']
state_machine = credentials ['state_machine']
banned_url_portion = '/api/management/status/fail2banbannedaddress'


expe_cluster = 'expe_cluster1'
url_cluster = 'url_cluster1'
new_items = []

i = 1
while expe_cluster in credentials:
    expe = credentials [expe_cluster]
    user_expe = credentials[expe][0]
    pass_expe = credentials[expe][1]
    ban_url_cluster1 = credentials[url_cluster]+banned_url_portion
    new_items_output=Expressway_cluster(ban_url_cluster1, user_expe, pass_expe, jailed_file, roomID, bearer, state_machine, today, new_items)
    i += 1
    print ('new_items_output in ipjail: ', new_items_output)
    expe_cluster = 'expe_cluster'+str(i)
    url_cluster = 'url_cluster'+str(i)
    new_items = new_items_output



print("STOP LINE --------------------------------------------------------")

