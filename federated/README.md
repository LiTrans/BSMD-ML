This experiment runs a federated learning algorithm with four nodes. All transactions are recorded in the BSMD and we use sockets for data transfers

The [hook.py](hook.py) file is based on the code made by [coMindOrg](https://comind.org) in particular we use the [federated-sockets](https://github.com/coMindOrg/federated-averaging-tutorials/tree/master/federated-sockets) example as reference.

# Setup

Generate a private key and a certificate with: `openssl req -new -x509 -days 365 -nodes -out server.pem -keyout server.key`

> `SSL_CONF.key_path = Path to your private key`

> `SSL_CONF.cert_path = Path to your certificate`

Set the paths `SSL_CONF.key_path`and `SSL_CONF.cert_path` where you store the private key and certificate

In the [config.py](config.py) file modify the line 
```python
network = IrohaGrpc('localhost:50051')
```
and replace localhost for the IP of a node running the BSMD.


In the [federated_classifier.py](federated_classifier.py) file modify the parameters 
```python
BATCH_SIZE = 32
EPOCHS = 5
INTERVAL_STEPS = 100 # Steps between averages
WAIT_TIME = 5 # How many seconds to wait for new workers to connect

# Set these IPs of the computer associated to the chief node
# for local testing use localhost
CHIEF_PUBLIC_IP = 'localhost:7777' # Public IP of the chief worker
CHIEF_PRIVATE_IP = 'localhost:7777' # Private IP of the chief worker
```

To setup the federated nodes run
```shell
python3 Setup.py
```


# Run experiment

On the chief computer run
```shell
python3 federated_classifier.py --is_chief=True --worker_name=chief
```

On the first worker computer run
```shell
python3 federated_classifier.py --is_chief=False --worker_name=worker1
```
On the second worker computer run
```shell
python3 federated_classifier.py --is_chief=False --worker_name=worker2
```

On the third worker computer run
```shell
python3 federated_classifier.py --is_chief=False --worker_name=worker3
```

On the fourth worker computer run
```shell
python3 federated_classifier.py --is_chief=False --worker_name=worker4
```

