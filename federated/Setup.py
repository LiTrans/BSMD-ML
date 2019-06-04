#!/usr/bin/env python3
import binascii
import sys
import iroha_functions
from iroha import IrohaCrypto
import iroha_config

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
    print(
        'Transaction hash = {}, creator = {}'.format(hex_hash, transaction.payload.reduced_payload.creator_account_id))
    iroha_config.network.send_tx(transaction)
    for status in iroha_config.network.tx_status_stream(transaction):
        print(status)


@trace
def create_domain_and_asset():
    """
    Create a domain, default user and define asset
    :return: null
    """
    commands = [iroha_config.iroha.command('CreateDomain', domain_id=iroha_config.domain_id,
                                           default_role=iroha_config.default_role),
        iroha_config.iroha.command('CreateAsset', asset_name=iroha_config.asset_name, domain_id=iroha_config.domain_id,
                                   precision=iroha_config.asset_precision)]
    tx = IrohaCrypto.sign_transaction(iroha_config.iroha.transaction(commands), iroha_config.admin_private_key)
    send_transaction_and_print_status(tx)


create_domain_and_asset()
##################################
# workers nodes setup
# ################################
# create an account in the network
# create_account_user('Tommy', 'key', 'federated', '5', fedcoin#federated)
iroha_functions.create_account_user(iroha_config.worker1_name, iroha_config.worker1_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker2_name, iroha_config.worker2_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker3_name, iroha_config.worker3_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker4_name, iroha_config.worker4_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker5_name, iroha_config.worker5_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker6_name, iroha_config.worker6_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker7_name, iroha_config.worker5_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker8_name, iroha_config.worker8_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker9_name, iroha_config.worker9_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)

##################################
# chief node setup
# ################################
# create an account in the network
iroha_functions.create_account_user(iroha_config.chief_name, iroha_config.chief_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)

##################################
# grant access
# ################################
# grant access so worker nodes can share us his information
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker1_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker2_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker3_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker4_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker5_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker6_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker7_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker8_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.network,
                                             iroha_config.chief_account_id, iroha_config.chief_private_key,
                                             iroha_config.worker9_account_id)

# grant access so worker node can share us his information
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker1, iroha_config.network,
                                             iroha_config.worker1_account_id, iroha_config.worker1_private_key,
                                             iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker2, iroha_config.network,
                                             iroha_config.worker2_account_id, iroha_config.worker2_private_key,
                                             iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker3, iroha_config.network,
                                             iroha_config.worker3_account_id, iroha_config.worker3_private_key,
                                             iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker4, iroha_config.network,
                                             iroha_config.worker4_account_id, iroha_config.worker4_private_key,
                                             iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker5, iroha_config.network,
                                             iroha_config.worker5_account_id, iroha_config.worker5_private_key,
                                             iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker6, iroha_config.network,
                                             iroha_config.worker6_account_id, iroha_config.worker6_private_key,
                                             iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker7, iroha_config.network,
                                             iroha_config.worker7_account_id, iroha_config.worker7_private_key,
                                             iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker8, iroha_config.network,
                                             iroha_config.worker8_account_id, iroha_config.worker8_private_key,
                                             iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker9, iroha_config.network,
                                             iroha_config.worker9_account_id, iroha_config.worker9_private_key,
                                             iroha_config.chief_account_id)

print('**********************************')
print('**********************************')
print('The BSMD is created and iroha_configured')
print('**********************************')
print('**********************************')
