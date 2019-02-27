# Create a domain, asset and default role in the BSMD network
The first step for setting up the BSMD is to create domain, define an asset and define a default role. To do so just run the [Setup.py](Setup.py) file.

The `setup.py` file creates a domain call **federated**, an asset call **fedcoin** and a default role call **user**. Domains are use to grup a set of users with common goals. For example, in this case all nodes will use the BSMD for participating in a Federated Learning algorithm, hence all nodes must be in the domain **federated**. A node can be part of different domains. **Assets** are virtual coins the **users** use for payments.

The `setup.py` file contain two function `send_transaction_and_print_status(transaction)` and `create_domain_and_asset()`. The first one is use for sending any transaction to the BSMD, while the second is use to configure the **domain**, default **role** and **assets**.

In the `create_domain_and_asset()` function modify the parameters `domain_id`, `default_role` and `asset_name` to setup a domain, default role and asset. Example
```python
commands = [
        iroha.command('CreateDomain', domain_id='federated', default_role='user'),
        iroha.command('CreateAsset', asset_name='fedcoin', domain_id='federated',precision=2)
        ]
```

The `precision` parameter is the number of decimals accepted in the assets. All assets with more decimals will be rounded to the neares number. 

`default_role` must be setting up first in the [genesis.block](/network/config/genesis.block) file. In this particular example we define the `user` role in the [genesis.block](/network/config/genesis.block) file as
```json
"createRole":{
        "roleName":"user",
        "permissions":[
                "can_add_signatory",
                "can_get_my_acc_ast",
                "can_get_my_acc_ast_txs",
                "can_get_my_acc_detail",
                "can_get_my_acc_txs",
                "can_get_my_account",
                "can_get_my_signatories",
                "can_get_my_txs",
                "can_grant_can_add_my_signatory",
                "can_grant_can_remove_my_signatory",
                "can_grant_can_set_my_account_detail",
                "can_grant_can_set_my_quorum",
                "can_grant_can_transfer_my_assets",
                "can_receive",
                "can_remove_signatory",
                "can_set_quorum",
                "can_transfer"
                ]
        }
```
# Functions

Node have some functionalities to interact with other nodes which are are described next. The first step for developing applications in the BSMD is the [creation of a node](#create-node) in the blockchain. The creation of a node is similar to the process of sign-in a web page. 

After a node is created he can transfers assets to other nodes, set parameters in his identity (set name, adders, etc), among others.

This function available in the BSMD are:
  * [Create Node](#create-node)
  * [Get balance](#get-balance)
  * [Transfers assets](#transfers-assets)
  * [Set details](#set-details)
  * [Grant permission to set details](#grant-permission-to-set-details)
  * [Get all details](#get-all-details)
  * [Get all details from a generator](#get-all-details-from-a-generator)
  * [Get a detail from a generator](#get-a-detail-from-a-generator)

## Create Node

To create nodes run the function 
```python
functions.create_account_user(name,user_public_key,domain,asset_qty,asset_id)
``` 
The parameters are:
- `name`: (string) Name of the node, each name in the BSMD need to be unique
- `user_public_key`: (string) public key of the node. The key is obtained with the function `IrohaCrypto.derive_public_key(user_private_key)`. **NOTE**: for this example the `user_private_key = b11224fedce8e8deebf4c03339f16790681f35ca09ccdc9785a7217394065af5`, but in production environments the private key must be obtained with the function`IrohaCrypto.private_key()`
- `domain`: (string) Name of the domain the user wants to join. The domain must correspond to a domain created in the [Setup.py](Setup.py). In this example the domain name is **federated**
- `asset_qty`: (float) Quantity of assets the node buy. Nodes can be created with a initial number of assets, for instance if a node wants to participate in the Blockchain he can add some money to his account to make transactions. 
- `asset_id`: (string) Name of asset the node buy. The id have the following form `asset_name#domain`, in this example the id is `fedcoin#federated`


## Get balance 

To know the balance of the node account use:
```python
get_balance(iroha,network,account_id,user_private_key)
```
This function returns an array with the assets quantity of the node account. Example:
```python
[asset_id: "fedcoin#federated"
account_id: "generator@federated"
balance: "1000"
]
```
Only the owner and the **admin** can query the owners assets. The parameters are:
- `iroha`: Address for connecting to a domain in the BSMD. The address have the following form `Iroha(name@domain)`. In this example the address is `Iroha(generator@federated)` 
- `network`: Physical address of one node running the BSMD. The address have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the address is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the BSMD runs in our local machine
-`account_id`: (string) Id of the user in the domain. The account_id have the following form `name@domain`. In this example the account_id is `generator@federated`
-`user_private_key`: (string) Private key of the user

## Transfers assets 
Assets can be transferred to other account in exchange for a service. Only the owner can transfer his assets. In the BSMD-ML nodes will pay other nodes to compute federated parameters. To transfer assets use:
```python
transfer_coin(iroha, network, account_id, private_key, destination_account, asset_id, quantity, description)
```
The parameters are:
- `iroha`: Address for connecting to a domain in the BSMD. The address have the following form `Iroha(name@domain)`. In this example the address is `Iroha(generator@federated)` 
- `network`: Physical address of one node running the BSMD. The address have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the address is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the BSMD runs in our local machine
- `account_id`: (account_id) Id of the account owner. The account_id have the following form `name@domain`
- `private_key`: (string) Private key of the user who sign the transaction
- `destination_account`: (acount_id) Id of the destination account. Example `dest_account@domain`
- `asset_id`: (asset_id) Id of the asset. Example `asset_name#domain`
- `quantity`: (float) Quantity of asset to be transferred
- `description`(string) Description of the transaction. Example 'payment for computing parameters'

## Set details
Nodes can set details regarding his identity and the information they own or generate. For example a the detail of a node could be personal information like name, address or gender. But details can also be information generated by the node such as: federated parameters, GPS traces, trip distances, visited locations, etc. 

Nodes can grant permission to other nodes to set some details in his account. Granting permissions is useful when a node generate some information and want to share/sell this information with another node (see [Grant permission to set details](#grant-permsion-to-set-details)).

To set detail use
```python
set_detail_to_node(iroha, network, account_id, private_key, detail_name, detail_value)
```
The parameters are:
- `iroha`: Address for connecting to a domain in the BSMD. The address have the following form `Iroha(name@domain)`. In this example the address is `Iroha(generator@federated)` 
- `network`: Physical address of one node running the BSMD. The address have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the address is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the BSMD runs in our local machine
- `account_id`: (account_id) Id of the user we want the set the details. The account_id have the following form `name@domain`
- `private_key`: (string) Private key of the user who is signing the transactions.
- `detail_id`: (string) Name of the detail we want to set. Example `address`, `name`, etc
- `detail_value`: (string) Value of the detail. Example `Quetzacoatl`, `123 Fake st.`, etc

**Note**: Previously created details will be overwritten

## Grant permission to set details
Nodes can grant other nodes permissions to set details in their identities. Granting this permission can be use as a way to share information. 

To grant permissions to set details use
```python
grants_access_to_set_details(iroha, network, my_id_account, private_key, grant_account_id)
```

The parameters are:
- `iroha`: Address for connecting to a domain in the BSMD. The address have the following form `Iroha(name@domain)`. In this example the address is `Iroha(generator@federated)` 
- `network`: Physical address of one node running the BSMD. The address have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the address is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the BSMD runs in our local machine
- `my_id_account`: (account_id) Id of the user who wants to grant the permission. The account_id have the following form `name@domain`
- `private_key`: (string) Private key of the user who is signing the transactions.
- `grant_account_id`: (account_id) Id of the user to which we are granting the permission. The account_id have the following form `name@domain`

## Get all details
To know all the details of the node use:
```python
get_all_details(iroha, network, account_id, private_key
```
This function returns a `json` with the details written by all the generators of information. The json contains the id of the node who generate the information and the information generated:
```json
{
   "nodeA@domain":{
      "Age":"35",
      "Name":"Quetzacolatl"
   },
   "nodeB@domain":{
      "Location":"35.3333535,-45.2141556464",
      "Status":"valid"
   },
   "nodeA@domainB":{
      "FederatingParam":"35.242553",
      "Loop":"3"
   }
}
```
The parameters are:
- `iroha`: Address for connecting to a domain in the BSMD. The address have the following form `Iroha(name@domain)`. In this example the address is `Iroha(generator@federated)` 
- `network`: Physical address of one node running the BSMD. The address have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the address is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the BSMD runs in our local machine
- `account_id`: (account_id) Id of the user. The account_id have the following form `name@domain`
- `private_key`: (string) Private key of the user who is signing the transactions

## Get all details from a generator
To know all the details written by a generator use:
```python
get_all_details_from_generator(iroha, network, account_id, private_key, generator_id):
```
This function returns a `json` with the details written by one generator. The json contains the id of the node who generate the information and the information generated:
```json
{
   "nodeA@domain":{
      "Age":"35",
      "Name":"Quetzacolatl"
   }
}
```
The parameters are:
- `iroha`: Address for connecting to a domain in the BSMD. The address have the following form `Iroha(name@domain)`. In this example the address is `Iroha(generator@federated)` 
- `network`: Physical address of one node running the BSMD. The address have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the address is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the BSMD runs in our local machine
- `account_id`: (account_id) Id of the user. The account_id have the following form `name@domain`
- `private_key`: (string) Private key of the user who is signing the transactions
- `generator_id`: (account_id) Private key of the user who create the detail. This account_id can be the same as the owner or can be the node who create the detail

## Get a detail from a generator
To know one detail written by a generator use:
```python
get_detail_from_generator(iroha, network, account_id, private_key, generator_id, detail_id):
```
This function returns a `json` with one detail written by one generator. The json contains the id of the node who generate the information and the information generated:
```json
{
   "nodeA@domain":{
      "Age":"35"
   }
}
```
The parameters are:
- `iroha`: Address for connecting to a domain in the BSMD. The address have the following form `Iroha(name@domain)`. In this example the address is `Iroha(generator@federated)` 
- `network`: Physical address of one node running the BSMD. The address have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the address is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the BSMD runs in our local machine
- `account_id`: (account_id) Id of the user. The account_id have the following form `name@domain`
- `private_key`: (string) Private key of the user who is signing the transactions
- `generator_id`: (account_id) Private key of the user who create the detail. This account_id can be the same as the owner or can be the node who create the detail
- `detail_id`: (string) Name of the detail we want to query
