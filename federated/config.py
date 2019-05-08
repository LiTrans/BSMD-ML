import hashlib
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto

#socket configuration
SEND_RECEIVE_CONF = lambda x: x
SEND_RECEIVE_CONF.key = b'4C5jwen4wpNEjBeq1YmdBayIQ1oD'
SEND_RECEIVE_CONF.hashfunction = hashlib.sha1
SEND_RECEIVE_CONF.hashsize = int(160 / 8)
SEND_RECEIVE_CONF.error = b'error'
SEND_RECEIVE_CONF.recv = b'reciv'
SEND_RECEIVE_CONF.signal = b'go!go!go!'
SEND_RECEIVE_CONF.buffer = 8192*2

SSL_CONF = lambda x: x
SSL_CONF.key_path = 'server.key'
SSL_CONF.cert_path = 'server.pem'



# BSMD configuration
######################
asset_id = 'fedcoin#federated'
# Replace localhost with an IP address of a node running the blockchain
network = IrohaGrpc('localhost:50051')
domain_id = 'federated'
admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
iroha = Iroha('admin@test')
default_role = 'user'
asset_name = 'fedcoin'
asset_precision = 2

#chief node
######################
chief_private_key = '054e294d86bedf9a43cf20542cade6e57addfd4294a276042be4ba83c73f8d9e'
chief_public_key = IrohaCrypto.derive_public_key(chief_private_key)
chief_name = 'chief'
chief_account_id = chief_name + '@' + domain_id
iroha_chief = Iroha('chief@federated')

#worker1 node
######################
worker1_private_key = '7a3a8efe3fbfac57af55e8d2a4b20e27b19444c4d240924dd1bd57701a5a0731'
worker1_public_key = IrohaCrypto.derive_public_key(worker1_private_key)
worker1_name = 'worker1'
worker1_account_id = worker1_name + '@' + domain_id
iroha_worker1 = Iroha('worker1@federated')

#worker2 node
######################
worker2_private_key = '94ba95a4520107a8a9abc864db900b5c00660c48bbb0333edaa5ab081f52e2ed'
worker2_public_key = IrohaCrypto.derive_public_key(worker2_private_key)
worker2_name = 'worker2'
worker2_account_id = worker2_name + '@' + domain_id
iroha_worker2 = Iroha('worker2@federated')

#worker3 node
######################
worker3_private_key = '8c578c774f553b99ebbaf89d9314f8ceaf6b4e93119c2550e10cf0de8ee93b51'
worker3_public_key = IrohaCrypto.derive_public_key(worker3_private_key)
worker3_name = 'worker3'
worker3_account_id = worker3_name + '@' + domain_id
iroha_worker3 = Iroha('worker3@federated')

#worker4 node
######################
worker4_private_key = 'afa0c9cd046cbf7cb8998761c28a3dbfd8537de02d078657dcce25614a34b2d9'
worker4_public_key = IrohaCrypto.derive_public_key(worker4_private_key)
worker4_name = 'worker4'
worker4_account_id = worker4_name + '@' + domain_id
iroha_worker4 = Iroha('worker4@choice')
