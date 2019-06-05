#!/usr/bin/env python3
import binascii
import sys
import iroha_functions
import iroha_config

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

iroha_functions.create_domain_and_asset()
#################################
# workers nodes setup
################################
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
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker1_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker2_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker3_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker4_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker5_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker6_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker7_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker8_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key,iroha_config.worker9_account_id)

# grant access so worker node can share us his information
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker1,iroha_config.worker1_account_id,
                                             iroha_config.worker1_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker2, iroha_config.worker2_account_id,
                                             iroha_config.worker2_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker3, iroha_config.worker3_account_id,
                                             iroha_config.worker3_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker4, iroha_config.worker4_account_id,
                                             iroha_config.worker4_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker5, iroha_config.worker5_account_id,
                                             iroha_config.worker5_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker6, iroha_config.worker6_account_id,
                                             iroha_config.worker6_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker7, iroha_config.worker7_account_id,
                                             iroha_config.worker7_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker8, iroha_config.worker8_account_id,
                                             iroha_config.worker8_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker9, iroha_config.worker9_account_id,
                                             iroha_config.worker9_private_key, iroha_config.chief_account_id)

print('**********************************')
print('**********************************')
print('The BSMD is created and iroha_configured')
print('**********************************')
print('**********************************')
