# Prerequisites

- Install Iroha python sdk
```shell
pip install iroha
```
# Create a domain, asset and default role in the BSMD network
```shell
python3 setup.py
```
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
# Create a node
```shell
python3 node.py
```
The `node.py` file creates a node call **generator** with role **user** in the domain **federated** and a credit of 1000 **fedcoins**. 

To create nodes run the function `functions.create_account_user(name,user_public_key,domain,asset_qty,asset_id)` with the following parameters:
- `name`: (string) Name of the node, each name in the BSMD need to be unique
- `user_public_key`: (string) public key of the node. The key is obtained with the function `IrohaCrypto.derive_public_key(user_private_key)`. NOTE: for this example the `user_private_key = b11224fedce8e8deebf4c03339f16790681f35ca09ccdc9785a7217394065af5`, but in production enviroments the private key must be obtained with the function`IrohaCrypto.private_key()`
- `domain`: (string) Name of the domain where the node is created. The domain must correspond to a domain created in the [Setup.py](Setup.py). In this example the domain name is **federated**
- `asset_qty`: (float) Initial assets of the node. Nodes can be created with a initial number of assets, for instance if a node wants to participate in the blockchain he can add some money to his account to make transactions. 
- `asset_id`: (string) Id of the asset we want to query. The id have the following form `asset_name#domain`, in this example the id is `fedcoin#federated`

## Functions

Node have some functionaties to interact with other nodes which are are desribed next:

### Get balance 
To know the balance of the node account use:
```python
functions.get_balance(iroha,network,account_id,user_private_key)
```
This function returns an array with the assets quantyt of the node account. Example:
```
[asset_id: "fedcoin#federated"
account_id: "generator@federated"
balance: "1000"
]
```
Only the owner and the **admin** can query the owners assets. The parameters are:
- `iroha`: Addres for connecting to a domain in the BSMD. The addres have the following form `Iroha(name@domain)`. In this example the addres is `Iroha(generator@federated)` 
- `network`: Phisical addres of one node runng the blockchain. The addres have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the addres is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the blockchain runs in our local machine
-`account_id`: (string) Id of the user in the domain. The account_id have the following form `name@domain`. In this example the account_id is `generator@federated`
-`user_private_key`: (string) Private key of the user

### Transfers assets 
Assets can be tranfered to other account in exchange for a service. Only the owner can tranfer his assets. In the BSMD-ML nodes will pay other nodes to compute federated parameters. To transfer assets use:
```python
transfer_coin(iroha, network, account_id, private_key, destination_account, asset_id, quantity, description)
```
The parameters are:
- `iroha`: Addres for connecting to a domain in the BSMD. The addres have the following form `Iroha(name@domain)`. In this example the addres is `Iroha(generator@federated)` 
- `network`: Phisical addres of one node runng the blockchain. The addres have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the addres is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the blockchain runs in our local machine
- `account_id`: (account_id) Id of the account owner. The account_id have the following form `name@domain`
- `private_key`: (string) Private key of the user who sign the transaction
- `destination_account`: (acount_id) Id of the desitination account. Example `dest_account@domain`
- `asset_id`: (asset_id) Id of the asset. Example `asset_name#domain`
- `quantity`: (float) Quantity of asset to be transfered
- `description`(string) Descrition of the transaction. Example 'payment for computing paramenters'

### Set details
Nodes can set information details regarding his identity and the information they own or generate. For example a the detail of a node could be personal inofrmation like name, addres or gender. But details can also be information generated by the node such as: federated paramenters, GPS traces, trip distances, visited locations, etc. 

Nodes can grant permission to other nodes to set some details in his account. Grantinng perssion is usefule when a node generate some inofrmation and want to share/sell this information with another node (see [Grant permsion to set details of a node](#grant-permsion-to-set-details-of-a-node)).

To set detail use
```python
set_detail_to_node(iroha, network, account_id, private_key, detail_name, detail_value)
```
The parameters are:
- `iroha`: Addres for connecting to a domain in the BSMD. The addres have the following form `Iroha(name@domain)`. In this example the addres is `Iroha(generator@federated)` 
- `network`: Phisical addres of one node runng the blockchain. The addres have the following form `IrohaGrpc(IP_of_the_node)`.  In this example the addres is `IrohaGrpc()` (or `IrohaGrpc(127.0.0.1)`) since the blockchain runs in our local machine
- `account_id`: (account_id) Id of the user we want the set the details. The account_id have the following form `name@domain`
- `private_key`: (string) Private key of the user who is singing the transactions.
- `detail_id`: (string) Name of the detail we want to set. Example `addres`, `name`, etc
- `detail_value`: (string) Value of the detail. Example `Quetzacoatl`, `123 Fake st.`, etc

**Note**: Previously created details will be overwriten
`
### Grant permsion to set details of a node

Bla bla
