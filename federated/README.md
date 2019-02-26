### Prerequisites

- Install Iroha python sdk
```shell
pip install iroha
```
### Create a domain, asset and default role in the BSMD network
```shell
python3 setup.py
```
The `setup.py` file creates a domain call **federated**, an asset call **fedcoin** and a default role call **user**. Domains are use to grup a set of users with common goals. For example, in this case all nodes will use the BSMD for participating in a Federated Learning algorithm, hence all nodes must be in the domain **federated**. A node can be part of different domains. **Assets** are virtual coins the **users** use for payments.

The `setup.py` file contain two function `send_transaction_and_print_status(transaction)` and `create_domain_and_asset()`. The first one is use for sending any transaction to the BSMD, while the second is use to configure the **domain**, default **role** and **assets**.

In the `create_domain_and_asset()` function modify the parameters `domain_id`, `default_role` and `asset_name` to setup a domain, default role and asset. 
```python
commands = [
	iroha.command('CreateDomain', domain_id='your_domain_name', default_role='your_defaul_role'),
	iroha.command('CreateAsset', asset_name='your_asset_name', domain_id='your_domain_name',precision=number_of_decimals)
	]
```
NOTE: `your_default_role` must be setting up first in the [genesis.block](/network/config/genesis.block) file. In this particular example we define the `user` role in the [genesis.block](/network/config/genesis.block) file as
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
