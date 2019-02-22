# Instruction for running the BSMD

1. Dowload the iroha binaries from this [link](https://www.dropbox.com/s/a886c3bl38qg5le/iroha.tar.xz?dl=0)
2. Uncompres the file in the network folder
3. Open the [config.sample](config/config.sample) file and change *host*, *port*, *user* and *password* to match your configuration
3. In terminal go to the "BSMD-ML/network/" folder and run
```
irohad --config config/config.sample --genesis_block config/genesis.block --keypair_name config/node0
```
4. Now you have a blockchain running on your machine. This blockchain is intended for testing and only have one node.


For stoping the network: `ctrl+c`

If you want to do a fresh start run
```
irohad --config config/config.sample --genesis_block config/genesis.block --keypair_name config/node0 --overwrite_ledger
```




