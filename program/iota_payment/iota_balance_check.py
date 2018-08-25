# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 00:07:33 2018

@author: Jannis
"""
### CREDITS https://medium.com/coinmonks/integrating-physical-devices-with-iota-83f4e00cc5bb

import time

# Import the PyOTA library
from iota import Iota
from iota import Address

def check_balance():
    '''
    Function for checking address balance on the IOTA tangle 
    returns current balance value (only approved transactions) 
    '''
    print("Checking Balance...")
    gb_result = api.get_balances(address)
    balance = gb_result['balances']
    return (balance[0])

def run(): 
    # Get current address balance at startup and use as baseline for measuring new funds being added 
    current_balance = check_balance()
    last_balance = current_balance
    while True:
        # Check for new funds
        current_balance = check_balance()
        if current_balance > last_balance:
            last_balance = current_balance
            print(current_balance)
            print("TRANSACTION RECEIVED")
            #serial.send(b'O') # Send opening signal to arduino
            print('Opening Barrier...')
            time.sleep(20) # Let car pass and barrier close (placeholder for serial connection to arduino), see next line
            #barrier_state = serial.read(ser.inWaiting()) # get barrier closed signal from arduino serial connection
            state = 'Searching Car' # Reset to former state, search for new car to arrive
            print('State:', state)
            break
        else:
            print(current_balance)
    
        # Pause for 1 sec.
        time.sleep(1)

    
if __name__ == "__main__":
    
    # URL to IOTA fullnode used when checking balance, please insert from public source
    iotaNode = "" # if own full node, http://localhost:14256
    # Create an IOTA object
    api = Iota(iotaNode, "")
    # IOTA address to be checked for new funds, insert own receiving address
    address = [Address(b'')]
         
    run()
