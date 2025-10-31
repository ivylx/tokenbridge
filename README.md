# Build a Token Bridge between Two EVM-compatible Blockchains(Avalanche and BSC testnets)
Repository for my EAS583 Blockchains, Summer 2024.

Ivy Xie (Individual)

### Description of Code and Layout
* Report: `Token bridge between two EVM-compatible blockchains Project Report.pdf`
* The `code/` folder under the root directory contains all the python, SOL and JSON files that I wrote for this project.

### Project Structure:

1.Created accounts on the Avalanche and BNB testnets, and signed messages
2.Created the contract on the destination side of the Bridge
3.Created the contract on the source side of the Bridge
4.Created an off-chain `listener` that could listen for events emitted by a contract

### Steps of Building a Token Bridge

1. Deploy the source contract to the source chain (Avalanche Testnet).
2. Deploy the destination contract to the destination chain (BNB Testnet)
3. Augment the `listener` so that when it hears an event from one of the bridge contracts, it calls the appropriate function on the other contract.
4. Call the `wrap()` function on the destination contract when the bridge sees the `Deposit` event emitted by the source contract. 
5. Call the `withdraw()` function on the source contract when the bridge sees the `Unwrap` event emitted by the destination contract. 
6. Deploy a `test` token on the Source side that can be bridged over.
7. Deploy the source and destination contracts and record their addresses, as well as the signing key of the deployer (the bridge `warden`).
8. Put the deploy addresses into contract_info.json which also contains the ABI of the contracts that will be useful.
9. Register the appropriate ERC20 tokens by calling the `registerToken()` function on the Source contract.
10. Call the `createToken()` function on the Destination contract with the two token relevant token addresses that are in the erc20s.csv.
11. Deposit events log three values, `token`, `to` and `amount`, along with the chain (either `avax` or `bsc`), the contract address and the transaction hash.

### Functions on Source and Destination sides

1.deposit():
 
*Check if the token being deposited has been `registered`.
*Use the ERC20 `transferFrom` function to pull the tokens into the deposit contract.
*Emit a `Deposit` event so that the bridge operator knows to make the necessary actions on the destination side.

2.withdraw():

*Check that the function is being called by the contract owner
*Push the tokens to the recipient using the ERC20 `transfer` function
*Emit a `Withdraw` event

3.registerToken():

*Check that the function is being called by the contract owner
*Check that the token has not already been registered
*Add the token address to the list of registered tokens
*Emit a Registration event

4.wrap():

*Mint deposited tokens on the source chain the correct BridgeToken on the destination chain.
*Only a `warden`, i.e., an address assigned the `WARDEN` role on the destination contract should be allowed to call this function. 
*Look up the BridgeToken that corresponds to the underlying asset and mint the correct amount of BridgeTokens to the recipient. 
*Check that underlying asset has been `registered,` i.e., that the owner of the destination contract has called createToken () on the underlying asset. 

5.unwrap():

*Burn BridgeToken by calling this function when a user wishes to return across the bridge.

### Privacy Considerations

Certain information, such as addresses, private keys, ABI, or sensitive configuration details, has been omitted from the files and replaced with `xxxx...` for privacy and security reasons.
---

## Acknowledgments
* EAS583 Instructors, TA's, and Ed
