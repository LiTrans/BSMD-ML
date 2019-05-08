#!/usr/bin/env python3
import binascii
import sys
import iroha_functions
from iroha import IrohaCrypto
import config
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


def trace(func):
    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result

    return tracer


@trace
def send_transaction_and_print_status(transaction):
    """
    Send a transaction to the Blockchain (BSMD)
    :param transaction: Transaction we are sending to the BSMD
    :param network: Address of the network we are sending the transaction
    :return: null
    """
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    config.network.send_tx(transaction)
    for status in config.network.tx_status_stream(transaction):
        print(status)


@trace
def create_domain_and_asset():
    """
    Create a domain, default user and define asset
    :return: null
    """
    commands = [
        config.iroha.command('CreateDomain', domain_id=config.domain_id, default_role=config.default_role),
        config.iroha.command('CreateAsset', asset_name=config.asset_name, domain_id=config.domain_id,
                             precision=config.asset_precision)
    ]
    tx = IrohaCrypto.sign_transaction(
        config.iroha.transaction(commands), config.admin_private_key)
    send_transaction_and_print_status(tx)


create_domain_and_asset()
##################################
# workers nodes setup
# ################################
# create an account in the network
# create_account_user('Tommy', 'key', 'federated', '5', fedcoin#federated)
iroha_functions.create_account_user(config.worker1_name, config.worker1_public_key, config.domain_id, '1000',
                                    config.asset_id)
iroha_functions.create_account_user(config.worker2_name, config.worker2_public_key, config.domain_id, '1000',
                                    config.asset_id)
iroha_functions.create_account_user(config.worker3_name, config.worker3_public_key, config.domain_id, '1000',
                                    config.asset_id)
iroha_functions.create_account_user(config.worker4_name, config.worker4_public_key, config.domain_id, '1000',
                                    config.asset_id)
##################################
# chief node setup
# ################################
# create an account in the network
iroha_functions.create_account_user(config.chief_name, config.chief_public_key, config.domain_id, '1000',
                                    config.asset_id)

##################################
# grant access
# ################################
# grant access so worker nodes can share us his information
iroha_functions.grants_access_to_set_details(config.iroha_chief, config.network, config.chief_account_id,
                                             config.chief_private_key, config.worker1_account_id)
iroha_functions.grants_access_to_set_details(config.iroha_chief, config.network, config.chief_account_id,
                                             config.chief_private_key, config.worker2_account_id)
iroha_functions.grants_access_to_set_details(config.iroha_chief, config.network, config.chief_account_id,
                                             config.chief_private_key, config.worker3_account_id)
iroha_functions.grants_access_to_set_details(config.iroha_chief, config.network, config.chief_account_id,
                                             config.chief_private_key, config.worker4_account_id)
# grant access so worker node can share us his information
iroha_functions.grants_access_to_set_details(config.iroha_worker1, config.network, config.worker1_account_id,
                                             config.worker1_private_key, config.chief_account_id)
iroha_functions.grants_access_to_set_details(config.iroha_worker2, config.network, config.worker2_account_id,
                                             config.worker2_private_key, config.chief_account_id)
iroha_functions.grants_access_to_set_details(config.iroha_worker3, config.network, config.worker3_account_id,
                                             config.worker3_private_key, config.chief_account_id)
iroha_functions.grants_access_to_set_details(config.iroha_worker4, config.network, config.worker4_account_id,
                                             config.worker4_private_key, config.chief_account_id)
print('**********************************')
print('**********************************')
print('The BSMD is created and configured')
print('**********************************')
print('**********************************')





# admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
# iroha = Iroha('admin@test')
# # set the ip of one node in the iroha blockchain
# asset_id = 'fedcoin#federated'
# domain_id = 'federated'
#
# ##################################
# # Set corresponding ip
# network = IrohaGrpc('localhost:50051')
# ##################################
#
# # function to create private keys
# # private_key = IrohaCrypto.private_key()
# #############################
# # Slaves node
# #############################
# # worker 1
# worker1_private_key = '7a3a8efe3fbfac57af55e8d2a4b20e27b19444c4d240924dd1bd57701a5a0731'
# worker1_public_key = IrohaCrypto.derive_public_key(worker1_private_key)
# worker1_name = 'worker1'
# worker1_account_id = worker1_name + '@' + domain_id
# worker1_iroha = Iroha('worker1@federated')
# # worker 2
# worker2_private_key = '94ba95a4520107a8a9abc864db900b5c00660c48bbb0333edaa5ab081f52e2ed'
# worker2_public_key = IrohaCrypto.derive_public_key(worker2_private_key)
# worker2_name = 'worker2'
# worker2_account_id = worker2_name + '@' + domain_id
# worker2_iroha = Iroha('worker2@federated')
# # worker 3
# worker3_private_key = '8c578c774f553b99ebbaf89d9314f8ceaf6b4e93119c2550e10cf0de8ee93b51'
# worker3_public_key = IrohaCrypto.derive_public_key(worker3_private_key)
# worker3_name = 'worker3'
# worker3_account_id = worker3_name + '@' + domain_id
# worker3_iroha = Iroha('worker3@federated')
# # worker 4
# worker4_private_key = 'afa0c9cd046cbf7cb8998761c28a3dbfd8537de02d078657dcce25614a34b2d9'
# worker4_public_key = IrohaCrypto.derive_public_key(worker4_private_key)
# worker4_name = 'worker4'
# worker4_account_id = worker4_name + '@' + domain_id
# worker4_iroha = Iroha('worker4@federated')
# ################################
# # chief node
# ################################
# chief_private_key = '054e294d86bedf9a43cf20542cade6e57addfd4294a276042be4ba83c73f8d9e'
# chief_public_key = IrohaCrypto.derive_public_key(chief_private_key)
# chief_name = 'chief'
# chief_account_id = chief_name + '@' + domain_id
# chief_iroha = Iroha('chief@federated')
