from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware #Necessary for POA chains
import json
import sys
import random
import string
import eth_account
from pathlib import Path

source_chain = 'avax'
destination_chain = 'bsc'
contract_info = "contract_info.json"

def connectTo(chain):
    if chain == 'avax':
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

    if chain == 'bsc':
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

    if chain in ['avax','bsc']:
        w3 = Web3(Web3.HTTPProvider(api_url))
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def getContractInfo(chain):
    """
        Load the contract_info file into a dictinary
        This function is used by the autograder and will likely be useful to you
    """
    p = Path(__file__).with_name(contract_info)
    try:
        with p.open('r')  as f:
            contracts = json.load(f)
    except Exception as e:
        print( "Failed to read contract info" )
        print( "Please contact your instructor" )
        print( e )
        sys.exit(1)

    return contracts[chain]



def scanBlocks(chain):
    """
        chain - (string) should be either "source" or "destination"
        Scan the last 5 blocks of the source and destination chains
        Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
        When Deposit events are found on the source chain, call the 'wrap' function the destination chain
        When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
    """

    if chain not in ['source','destination']:
        print( f"Invalid chain: {chain}" )
        return
    
        #YOUR CODE HERE

    w3s = Web3(Web3.HTTPProvider(f"https://api.avax-test.network/ext/bc/C/rpc"))
    w3d = Web3(Web3.HTTPProvider(f"https://data-seed-prebsc-1-s1.binance.org:8545/"))
    # inject the poa compatibility middleware to the innermost layer
    w3s.middleware_onion.inject(geth_poa_middleware, layer=0)
    w3d.middleware_onion.inject(geth_poa_middleware, layer=0)

    private_key = 'xxxx...'

    signer_s = w3s.eth.account.from_key(private_key)
    signer_d = w3d.eth.account.from_key(private_key)

    sourceAddr = "xxxx..."
    destinationAddr = "xxxx..."

    sourceContract = w3s.eth.contract(address=sourceAddr, abi=getContractInfo('source')['abi'])
    destContract = w3d.eth.contract(address=destinationAddr, abi=getContractInfo('destination')['abi'])

    arg_filter = {}

    end_block_s = w3s.eth.get_block_number()
    start_block_s = end_block_s - 10

    end_block_d = w3d.eth.get_block_number()
    start_block_d = end_block_d - 10
    
    if chain == 'source':
      event_filter_D = sourceContract.events.Deposit.create_filter(fromBlock=start_block_s,toBlock=end_block_s,argument_filters=arg_filter)
      events_D = event_filter_D.get_all_entries()
      for evt in events_D:
        contract_tx_d = destContract.functions.wrap(evt.args['token'], 
        evt.args['recipient'], evt.args['amount']).build_transaction({
          "from": signer_d.address,
          "nonce": w3d.eth.get_transaction_count(signer_d.address),
        })
        signed_tx_d = w3d.eth.account.sign_transaction(contract_tx_d, private_key=private_key)
        w3d.eth.send_raw_transaction(signed_tx_d.rawTransaction)
    if chain == 'destination':
      event_filter_U = destContract.events.Unwrap.create_filter(fromBlock=start_block_d,toBlock=end_block_d,argument_filters=arg_filter)
      events_U = event_filter_U.get_all_entries()
      for evt in events_U:
        contract_tx_s = sourceContract.functions.withdraw(evt.args['underlying_token'], 
        evt.args['to'], evt.args['amount']).build_transaction({
          "from": signer_s.address,
          "nonce": w3s.eth.get_transaction_count(signer_s.address),
        })
        signed_tx_s = w3s.eth.account.sign_transaction(contract_tx_s, private_key=private_key)
        w3s.eth.send_raw_transaction(signed_tx_s.rawTransaction)

        
      

