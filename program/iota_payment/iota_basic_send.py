# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 00:46:59 2018

@author: Jannis
"""

import iota
from iota import Iota
from iota import Address

# new seed generator !!!Caution!!!
import random
chars=u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ' #27 characters - max number you can express by one Tryte - do you remember?
rndgenerator = random.SystemRandom() #cryptographically secure pseudo-random generator
NewSeed = u''.join(rndgenerator.choice(chars) for _ in range(81)) #generating 81-chars long seed. This is Python 3.6+ compatible
print(NewSeed)
print("Length: %s" % len(NewSeed))


send_seed = "" # Insert own sending seed
send_addr = "" # INsert own sending address

recv_seed = "" # Insert own receiving seed, ofc not necessary for receiving purpose, only needed for generating new receiving address (see below)
recv_addr = "" # Insert own receiving address

# Node setup
uri = "" # Insert node URL
depth = 3     
api = iota.Iota(uri, seed=send_seed)

'''
# Node health check
api=iota.Iota(uri) # ctor initialization of the PyOTA library
result = api.get_node_info() # basic API call to double check health conditions
print(result) # result is printed out

# Basic check whether node is in sync or not
# Elementary rule is that "latestMilestoneIndex" should equal to "latestSolidSubtangleMilestoneIndex" or be very close
if abs(result['latestMilestoneIndex'] - result['latestSolidSubtangleMilestoneIndex']) > 3 :
    print ("\r\nNode is probably not synced!")
else:
    print ("\r\nNode is probably synced!")
'''

# Check balance
sender_account = api.get_account_data(start=0, stop=None)
sender_account["balance"]

# Generate new receiving address if needed
api = iota.Iota(uri, seed=recv_seed)
gna_result = api.get_new_addresses(count=1)
addresses = gna_result['addresses']
receiver_address = addresses[0]
print("Receiver address 0 is: " + str(receiver_address))


# Make transaction
proposedTransaction = iota.ProposedTransaction(address = iota.Address(recv_addr), value = 1)

print('Making transaction...')
transfer = api.send_transfer(transfers = [proposedTransaction], depth = depth, min_weight_magnitude=14,
             inputs = [iota.Address(send_addr, key_index=0, security_level=2)])

transactionHash = []
for transaction in transfer["bundle"]:
    transactionHash.append(transaction.hash)
    print(transaction.address, transaction.hash)
    
api.get_latest_inclusion(transactionHash)
#api.replay_bundle(transactionHash[0], depth=depth)