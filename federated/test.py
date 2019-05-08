import iroha_functions
import config
import json


transaction_data = dict()
transaction_data['Received from'] = '1'
transaction_data['Epoch'] = 1
transaction_data['iter'] = 100
transaction_data['accuracy'] = 100
transaction_data['loss'] = 100
json = json.dumps(transaction_data)
json_in_ledger = str(json)
j = json_in_ledger.replace('"','')
print(json_in_ledger.replace('"',''))

iroha_functions.set_detail_to_node(config.iroha_chief, config.network, config.worker1_account_id,
                                   config.chief_private_key, 'chiefefd', j)

# iroha_functions.get_block(122)
