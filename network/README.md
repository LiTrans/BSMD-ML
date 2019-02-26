# Instructions for running the BSMD (QUICK)

1. Download the Iroha binaries from this [link](https://www.dropbox.com/s/a886c3bl38qg5le/iroha.tar.xz?dl=0)
2. Decompress the file in the 'network' folder
3. Open the [config.sample](config/config.sample) file and change *host*, *port*, *user* and *password* to match your configuration
3. Open a terminal, go to the 'network' folder and run
```
irohad --config config/config.sample --genesis_block config/genesis.block --keypair_name config/node0
```
4. Now you have a Blockchain running on your machine. This Blockchain is intended for testing and only have one node.

## Additional commands
- For stopping the network: `ctrl+c`
- If you want to do a fresh start run
```
irohad --config config/config.sample --genesis_block config/genesis.block --keypair_name config/node0 --overwrite_ledger
```
# Instructions for running the BSMD (not so quick)
All files in the [config](/config) folder are not meant to be use in production environments, but can be use as guide for setting up a production environment. 

To run the BSMD in the [config](config/) folder create the following files:
1. [config.sample](config/config.sample). This file cotains the internal configuration of Iroha. For a complete guide of all paramentes read the [iroha configuration guide](https://iroha.readthedocs.io/en/master/guides/configuration.html)  
    1. `block_store_path`: sets path to the folder where blocks are stored.
    2. `torii_port sets`: the port for external communications. Queries and transactions are sent here.
    3. `internal_port`: sets the port for internal communications: ordering service, consensus and block loader.
    4. `pg_opt is used`: for setting credentials of PostgreSQL: hostname, port, username and password
2. [genesis.block](config/genesis.block). In the genesis file is possible to define a domain, adminstration accounts, users account, assets and define roles. This file is a valid `json` structure. Roles are important beacuse they define the permission a user will have for using the Blockchain. For a complete guide of permissions [read this guide](https://iroha.readthedocs.io/en/master/maintenance/permissions.html). In this example 3 roles are created: **admin**, **user** and **money creator**. The **admin** user have admin and money creator  roles, wich mean user **admin** has administrator privileges and can also create and transfers assets.  
1. [admin@test.priv](config/admin@test.priv). Private key of the administrator, this key is use to sign all transactions in the BSMD 
2. [admin@test.pub](config/admin@test.pub). Public key of the administrator, this key is use to identyfy the adminstrator in the BSMD
1. [node0.priv](config/node0.priv). Private key of node0. Node0 is use to create the network but has no other use, this node is not part of the BSMD 
2. [node0.pub](config/node0.pub). Public key of node0
