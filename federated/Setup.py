#!/usr/bin/env python3
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
import binascii
import sys
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
iroha = Iroha('admin@test')
net = IrohaGrpc()


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
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
        print(status)


# Create a domain and and define asset
@trace
def create_domain_and_asset():
    commands = [
        iroha.command('CreateDomain', domain_id='federated', default_role='user'),
        iroha.command('CreateAsset', asset_name='fedcoin', domain_id='federated', precision=2)
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), admin_private_key)
    send_transaction_and_print_status(tx)


create_domain_and_asset()
print('done')
