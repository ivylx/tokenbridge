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

contract_info = "contract_info.json"

def getContractInfo():
  cur_dir = Path(__file__).parent.absolute()
  with open(cur_dir.joinpath("contract_info.json"), "r") as f:
    d = json.load(f)
    #d = d[chain]
  return d['source']['abi']

def register():

  api_url = f"https://api.avax-test.network/ext/bc/C/rpc"

  w3 = Web3(Web3.HTTPProvider(api_url))
  
  w3.middleware_onion.inject(geth_poa_middleware, layer=0)

  private_key = 'xxxx...'

  signer = w3.eth.account.from_key(private_key)

  address = 'xxxx...'

  abi = getContractInfo()

  addressA = 'xxxx...'
  addressB = 'xxxx...'

  contract = w3.eth.contract(address=address, abi=abi) 

  contract_tx_A = contract.functions.registerToken(addressA).build_transaction({
    "from": signer.address,
    "nonce": w3.eth.get_transaction_count(signer.address),
  })
  signed_tx_A = w3.eth.account.sign_transaction(contract_tx_A, private_key=private_key)
  tx_hash_A = w3.eth.send_raw_transaction(signed_tx_A.rawTransaction)

  contract_tx_B = contract.functions.registerToken(addressB).build_transaction({
    "from": signer.address,
    "nonce": w3.eth.get_transaction_count(signer.address),
  })
  signed_tx_B = w3.eth.account.sign_transaction(contract_tx_B, private_key=private_key)
  tx_hash_B = w3.eth.send_raw_transaction(signed_tx_B.rawTransaction)

  print("Tokens registered!")

  return tx_hash_A, tx_hash_B

if __name__ == "__main__":
  register()