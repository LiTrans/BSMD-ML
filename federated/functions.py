#!/usr/bin/env python3
from iroha.primitive_pb2 import can_set_my_account_detail
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
import binascii
import sys
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'

def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """
    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result
    return tracer

# This function send a transaction to the blockchain
@trace
def send_transaction_and_print_status(transaction, network):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    network.send_tx(transaction)
    for status in network.tx_status_stream(transaction):
        print(status)


# Use the function to create a personal account. The account is created with the credit the user has
@trace
def create_account_user(name, public_key, domain_id, asste_qty, asset_id):
    iroha = Iroha('admin@test')
    network = IrohaGrpc()
    tx = iroha.transaction(
        [iroha.command('CreateAccount',
                       account_name=name,
                       domain_id=domain_id,
                       public_key=public_key)])
    IrohaCrypto.sign_transaction(tx, admin_private_key)
    send_transaction_and_print_status(tx, network)

    # Create credit for the user
    tx = iroha.transaction([iroha.command('AddAssetQuantity',
                                          asset_id=asset_id,
                                          amount=asste_qty)])
    IrohaCrypto.sign_transaction(tx, admin_private_key)
    send_transaction_and_print_status(tx, network)

    # Transfer credit to the user
    dest_account_id = name + '@' + domain_id
    tx = iroha.transaction([
        iroha.command('TransferAsset',
                      src_account_id='admin@test',
                      dest_account_id=dest_account_id,
                      asset_id=asset_id,
                      description='initial credit',
                      amount=asste_qty)])
    IrohaCrypto.sign_transaction(tx, admin_private_key)
    send_transaction_and_print_status(tx, network)

# Get the balance of the account
@trace
def get_balance(iroha, network, account_id, private_key):
    """
    List all the assets of userone@domain
    """
    query = iroha.query('GetAccountAssets',
                        account_id=account_id)
    IrohaCrypto.sign_query(query, private_key)

    response = network.send_query(query)
    data = response.account_assets_response.account_assets
    for asset in data:
        print('Asset id = {}, balance = {}'.format(asset.asset_id, asset.balance))
    return data

# granting access to write federating weights in own identity.
# This function is use after the node compute a weight. The node that compute the paramenter writ down
# the weight in the details of the collector
@trace
def grants_access_to_set_details(iroha, network, my_id_account, private_key, grant_account_id):
    tx = iroha.transaction([
        iroha.command('GrantPermission',
                      account_id=grant_account_id,
                      permission=can_set_my_account_detail)
    ],
        creator_account=my_id_account)
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx, network)


# Set computed weight to a node.
@trace
def set_detail_to_node(iroha, network, account_id, private_key, detail_key, detail_value):
    tx = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id,
                      key=detail_key,
                      value=detail_value)
    ])
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx, network)


# Transfer assets from one account to another
@trace
def transfer_coin(iroha, network, account_id, private_key, destination_account, asset_id, quantity, description):
    tx = iroha.transaction([
        iroha.command('TransferAsset',
                      src_account_id=account_id,
                      dest_account_id=destination_account,
                      asset_id=asset_id,
                      description=description,
                      amount=quantity)
    ])
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx, network)

# This function is use when a node wants to consult the weight of other participants
# Returns solicited information
@trace
def get_details_from(iroha, network, account_id, private_key, generator, detail_id):
    """
    Get asset info for coin#domain
    :return:
    """
    query = iroha.query('GetAccountDetail',
                        account_id=account_id,
                        writer=generator,
                        key=detail_id)
    IrohaCrypto.sign_query(query, private_key)

    response = network.send_query(query)
    # print(response)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format('generator@federating', data.detail))
    return data.detail



