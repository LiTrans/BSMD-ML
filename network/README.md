# Install Iroha

Iorha is installed in 4 _t3.medium_ Amazon cloud EC2 virtual machines with 2cores at 3.1GHz and 4GB of RAM. 

## Instructions
In terminal do
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y --no-install-recommends install apt-utils software-properties-common wget
sudo add-apt-repository -y ppa:git-core/ppa
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add -
sudo nano /etc/apt/sources.list
```
In nano add the following lines at the end of the file
```
deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-7 main
deb-src http://apt.llvm.org/bionic/ llvm-toolchain-bionic-7 main
```
In terminal do
```
sudo apt-get update

sudo apt-get -y --no-install-recommends install software-properties-common automake libtool build-essential clang-6.0 lldb-6.0 lld-6.0 g++-7 libssl-dev zlib1g-dev libcurl4-openssl-dev libc6-dbg golang git ssh tar gzip ca-certificates gnupg python-pip python3-pip python3-setuptools python-dev curl file gdb gdbserver ccache gcovr cppcheck doxygen rsync graphviz libgraphviz-dev unzip vim zip; sudo apt-get -y clean

sudo apt install postgresql postgresql-contrib
```
Configure postgres
```
sudo passwd postgres
```
Set a pasword #(recommend for testing "postgres")
```
su - postgres
psql -d template1 -c "ALTER USER postgres WITH PASSWORD 'postgres';"
exit

sudo nano /etc/postgresql/10/main/postgresql.conf
```
In nano search a uncomment line
```
max_prepared_transactions = 100
```
Download [dependicies](https://www.dropbox.com/s/6f8azu8yotcz5ic/dependencies.zip?dl=0) package and [iroha](https://www.dropbox.com/s/a886c3bl38qg5le/iroha.tar.xz?dl=0) installation file

In terminal
```
unzip build-deb.zip -d /home/ubuntu

sudo unzip dependencies.zip -d /opt

nano ~/.bashrc
```
In nano add the following lines at the end of the file
```
export PATH=$PATH:/home/ubuntu/build/bin
export PATH="$PATH:$HOME/bin"
```
In terminal
```
source ~/.bashrc

sudo dpkg -i /home/ubuntu/build/iroha-0x731d2c7afb5829f9ff716e4b8ff2bc986caca870-Linux.deb
sudo apt --fix-broken install
sudo dpkg -i /home/ubuntu/build/iroha-0x731d2c7afb5829f9ff716e4b8ff2bc986caca870-Linux.deb

sudo cp /opt/dependencies/soci/lib64/libsoci_core.so.3.2 /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/soci/lib64/libsoci_postgresql.so.3.2 /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/grpc/lib/libgrpc.so /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/grpc/lib/libgpr.so /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/c-ares/lib/libcares.so.2 /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/grpc/lib/libaddress_sorting.so /usr/lib/x86_64-linux-gnu/
```

# Run Iroha
On each machine do the following
1. Open the [genesis.block](genesis.block) file and update the 'address' entry to correspond the ip of each machine. For example, the entry:
```json
"peer":{
        "address":"99.230.31.239:10001",
        "peerKey":"bddd58404d1315e0eb27902c5d7c8eb0602c16238f005773df406bc191308929"
        }
                             
```
will correspond to node0. Inspect the file [node0.pub](node0.pub) and see that `peerkey` is the same key written in [node0.pub](node0.pub) file. Update all `peer` entries with the corresponding ip address and 'nodeN.pub' key


1. One each machine create the folder `config` and copy the [genesis.block](genesis.block) and the [config.sample](config.sample)

3. On each machine run (change 'node0' to make it correspond with the machine, i.e., machine 2 is node1, machine 3 is node2 and so on)
```
irohad --config config/config.sample --genesis_block config/genesis.block --keypair_name config/node0
```

## Aditional Commands
If you like to clean and start fresh
```
irohad --config config/config.sample --genesis_block config/genesis.block --keypair_name config/node0 --overwrite_ledger
```


