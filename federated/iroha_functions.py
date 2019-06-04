#!/usr/bin/env python3
from iroha.primitive_pb2 import can_set_my_account_detail
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
import binascii
import iroha_config
import sys
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')




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



@trace
def send_transaction_and_print_status(transaction, network):
    """
    Send a transaction to the Blockchain (BSMD)
    :param transaction: Transaction we are sending to the BSMD
    :param network: Address of the network we are sending the transaction
    :return: null:
    """
    # print(transaction)
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    network.send_tx(transaction)
    for status in network.tx_status_stream(transaction):
        print(status)



@trace
def create_account_user(name, public_key, domain_id, asset_qty, asset_id):
    """
    Create a personal account. This function works in three steps
        1. Create an account with a name, in a domain and a public key
        2. The admin create credit (assets) for the account (credit is created only if the user
           buy it)
        3. The admin transfer the credit to the user
    :param name: (str) Name of the node we are creating
    :param public_key: (str) public key of the node
    :param domain_id: (str) Name of the domain the user wants to join
    :param asset_qty: (float) Quantity of assets the node buy
    :param asset_id: (name#domain) Name of asset the node buy
    :return: null:

    Usage example:
    create_account_user('Tommy', 'key', 'federated', '5', fedcoin#federated)
    """
    # 1. Create account
    iroha = Iroha('admin@test')
    network = IrohaGrpc()
    tx = iroha.transaction(
        [iroha.command('CreateAccount',
                       account_name=name,
                       domain_id=domain_id,
                       public_key=public_key)])
    IrohaCrypto.sign_transaction(tx, iroha_config.admin_private_key)
    send_transaction_and_print_status(tx, network)

    # 2. Create credit for the user
    tx = iroha.transaction([iroha.command('AddAssetQuantity',
                                          asset_id=asset_id,
                                          amount=asset_qty)])
    IrohaCrypto.sign_transaction(tx, iroha_config.admin_private_key)
    send_transaction_and_print_status(tx, network)

    # 3. Transfer credit to the user
    dest_account_id = name + '@' + domain_id
    tx = iroha.transaction([
        iroha.command('TransferAsset',
                      src_account_id='admin@test',
                      dest_account_id=dest_account_id,
                      asset_id=asset_id,
                      description='initial credit',
                      amount=asset_qty)])
    IrohaCrypto.sign_transaction(tx, iroha_config.admin_private_key)
    send_transaction_and_print_status(tx, network)


@trace
def get_balance(iroha, network, account_id, private_key):
    """
    Get the balance of the account
    :param iroha: (Iroha('name@domain')) Address for connecting to a domain
    :param network: (IrohaGrpc('IP address')) Physical address of one node running the BSMD
    :param account_id: (name@domain) Id of the user in the domain
    :param private_key: (str) Private key of the user
    :return: data: (array) asset id and assets quantity

    Usage example:
    get_balance(Iroha('david@federated'), IrohaGrpc('127.0.0.1'), 'david@federated', 'key')

    Return example:
    [asset_id: "fedcoin#federated"
    account_id: "generator@federated"
    balance: "1000"
    ]
    """
    query = iroha.query('GetAccountAssets',
                        account_id=account_id)
    IrohaCrypto.sign_query(query, private_key)

    response = network.send_query(query)
    data = response.account_assets_response.account_assets
    for asset in data:
        print('Asset id = {}, balance = {}'.format(asset.asset_id, asset.balance))
    return data


@trace
def grants_access_to_set_details(iroha, network, my_id_account, private_key, grant_account_id):
    """
    Grant access to write details in own identity
    :param iroha: (Iroha('name@domain')) Address for connecting to a domain
    :param network: (IrohaGrpc('IP address')) Physical address of one node running the BSMD
    :param my_id_account: (name@domain) Id of the user granting the access
    :param private_key: (str) Private key of the user granting the access
    :param grant_account_id: (name@domain) Id of the user we want to grant the access
    :return: null:

    Usage example:
    grants_access_to_set_details(Iroha('david@federated'),IrohaGrpc('127.0.0.1'), 'david@federated','key',
                                'juan@federated')
    """
    tx = iroha.transaction([
        iroha.command('GrantPermission',
                      account_id=grant_account_id,
                      permission=can_set_my_account_detail)
    ],
        creator_account=my_id_account)
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx, network)


@trace
def set_detail_to_node(iroha, network, account_id, private_key, detail_key, detail_value):
    """
    Set the details of a node. In federated learning the details are in JSON format and
    contains the address (location) where the weight is stored (if the weight is small enough it can be
    embedded to the block if needed)
    :param iroha: (Iroha('name@domain')) Address for connecting to a domain
    :param network: (IrohaGrpc('IP address')) Physical address of one node running the BSMD
    :param account_id: (name@domain) Id of the user in the domain
    :param private_key: (str) Private key of the user
    :param detail_key: (str) Name of the detail we want to set
    :param detail_value: (str) Value of the detail
    :return: null:

    Usage example:
    set_detail_to_node(Iroha('david@federated'),IrohaGrpc('127.0.0.1'), 'david@federated', 'key', 'age', '33')
    """
    tx = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id,
                      key=detail_key,
                      value=detail_value)
    ])
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx, network)


@trace
def transfer_assets(iroha, network, account_id, private_key, destination_account, asset_id, quantity, description):
    """
    Transfer assets from one account to another
    :param iroha: (Iroha(name@domain)) Address for connecting to a domain
    :param network: (IrohaGrpc(IP address)) Physical address of one node running the BSMD
    :param account_id: (name@domain) Id of the user in the domain
    :param private_key: (str) Private key of the user
    :param destination_account: (name@domain) Id of the destination account
    :param asset_id: (name#domain) Id of the asset we want to transfer
    :param quantity: (float) Number of assets we want to transfer
    :param description: (str) Small message to the receiver of assets
    :return: null:

    Usage example:
    transfer_assets(Iroha('david@federated'),IrohaGrpc('127.0.0.1'), 'david@federated', 'key',
                    'toro@federated', 'fedcoin#federated', '2', 'Shut up and take my money')
    """
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


@trace
def get_detail_from_generator(iroha, network, account_id, private_key, generator_id, detail_id):
    """
    Consult a single detail writen by some generator
    :param iroha: (Iroha(name@domain)) Address for connecting to a domain
    :param network: (IrohaGrpc(IP address)) Physical address of one node running the BSMD
    :param account_id: (name@domain) Id of the user in the domain
    :param private_key: (str) Private key of the user
    :param generator_id: (name@domain) Id of the user who create de detail
    :param detail_id: (string) Name of the detail
    :return: data: (json) solicited details of the user

    Usage example:
    get_detail_from_generator(Iroha('david@federated'),IrohaGrpc('127.0.0.1'), 'david@federated', 'key',
                                'david@federated', 'Address')

    Return example:
    {
       "nodeA@domain":{
             "Age":"35"
        }
    }
    """
    query = iroha.query('GetAccountDetail',
                        account_id=account_id,
                        writer=generator_id,
                        key=detail_id)
    IrohaCrypto.sign_query(query, private_key)

    response = network.send_query(query)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return data.detail


@trace
def get_all_details_from_generator(iroha, network, account_id, private_key, generator_id):
    """
    Consult all the details generated by some node
    :param iroha: (Iroha(name@domain)) Address for connecting to a domain
    :param network: (IrohaGrpc(IP address)) Physical address of one node running the BSMD
    :param account_id: (name@domain) Id of the user in the domain
    :param private_key: (str) Private key of the user
    :param generator_id: (name@domain) Id of the user who create de detail
    :return: data: (json) solicited details of the user

    Usage example:
    get_detail_from_generator(Iroha('david@federated'),IrohaGrpc('127.0.0.1'), 'david@federated', 'key',
                              'david@federated')

    Return example:
    {
       "nodeA@domain":{
            "Age":"35",
            "Name":"Quetzacolatl"
        }
    }
    """

    query = iroha.query('GetAccountDetail',
                        account_id=account_id,
                        writer=generator_id)
    IrohaCrypto.sign_query(query, private_key)

    response = network.send_query(query)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return data.detail



@trace
def get_all_details(iroha, network, account_id, private_key):
    """
    Consult all details of the node
    :param iroha: (Iroha(name@domain)) Address for connecting to a domain
    :param network: (IrohaGrpc(IP address)) Physical address of one node running the BSMD
    :param account_id: (name@domain) Id of the user in the domain
    :param private_key: (str) Private key of the user
    :return: data: (json) solicited details of the user

    Usage example:
    get_detail_from_generator(Iroha('david@federated'),IrohaGrpc('127.0.0.1'), 'david@federated', 'key')

    Return example:
    {
        "nodeA@domain":{
            "Age":"35",
            "Name":"Quetzacoatl"
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
    """
    query = iroha.query('GetAccountDetail',
                        account_id=account_id)
    IrohaCrypto.sign_query(query, private_key)

    response = network.send_query(query)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return data.detail


@trace
def get_block(height):
    """
    Get the balance of the account
    :param iroha: (Iroha('name@domain')) Address for connecting to a domain
    :param network: (IrohaGrpc('IP address')) Physical address of one node running the BSMD
    :param account_id: (name@domain) Id of the user in the domain
    :param private_key: (str) Private key of the user
    :return: data: (array) asset id and assets quantity

    Usage example:
    get_balance(Iroha('david@federated'), IrohaGrpc('127.0.0.1'), 'david@federated', 'key')

    Return example:
    [asset_id: "fedcoin#federated"
    account_id: "generator@federated"
    balance: "1000"
    ]
    """
    iroha_config.iroha.blocks_query()
    query = iroha_config.iroha.query('GetBlock',
                        height=height)
    IrohaCrypto.sign_query(query, iroha_config.admin_private_key)

    block = iroha_config.network.send_query(query)
    print(block)
    return block

