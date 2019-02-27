#!/usr/bin/env python3
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
import sys
import functions
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


# user_private_key = IrohaCrypto.private_key()
user_private_key = 'b11224fedce8e8deebf4c03339f16790681f35ca09ccdc9785a7217394065af5'
user_public_key = IrohaCrypto.derive_public_key(user_private_key)
name = 'generator'
domain_id = 'federated'
account_id = name + '@' + domain_id
iroha = Iroha('generator@federated')
asset_id = 'fedcoin#federated'
network = IrohaGrpc()


functions.create_account_user(name,user_public_key,domain_id,'1000',asset_id)

data = functions.get_balance(iroha,network,account_id,user_private_key)



# functions.set_detail_to_node()
print('Resultados')
print(data)


