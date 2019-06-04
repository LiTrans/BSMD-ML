This experiment runs a federated learning algorithm with 10 nodes, 1 chief and 9 workers. In broad terms the experiment follows the next steps.
1. The chief node opens a connection socket and send the trained model to the workers nodes 
2. Ther worker nodes re-train the model with their local data and send the results to the chief node
3. The chief node averages the results and send the average to all workers
4. Step 2 and 3 are repeated until EPOCH = 100

All transactions are recorded in the BSMD and we use sockets for data transfers

The [hook.py](hook.py) file is based on the code made by [coMindOrg](https://comind.org) in particular we use the [federated-sockets](https://github.com/coMindOrg/federated-averaging-tutorials/tree/master/federated-sockets) example as reference.

# Setup

Generate a private key and a certificate with: `openssl req -new -x509 -days 365 -nodes -out server.pem -keyout server.key`

In the [iroha_config.py](iroha_config.py) file modify the lines 

```python
SSL_CONF.key_path = Path/to/your/private_key
SSL_CONF.cert_path = Path/to/your/certificate
.
.
.
network = IrohaGrpc('localhost:50051') # replace localhost for the IP of one of the nodes running the BSMD
```


In the [federated_classifier.py](federated_classifier.py) file modify the parameters 
```python
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

You can run the experiment en 10 RPIs or PC. However you can also run the experiment in different shells.

On the chief computer run
```shell
python3 federated_classifier.py --is_chief=True --worker_name=chief --file_X=X_Worker_1 --file_Y=Y_Worker_1
```

On the first worker computer run
```shell
python3 federated_classifier.py --is_chief=False --worker_name=worker1 --file_X=X_Worker_2 --file_Y=Y_Worker_2
```
On the second worker computer run
```shell
python3 federated_classifier.py --is_chief=False --worker_name=worker2 --file_X=X_Worker_3 --file_Y=Y_Worker_3 
```

On the third worker computer run
```shell
python3 federated_classifier.py --is_chief=False --worker_name=worker3  --file_X=X_Worker_4 --file_Y=Y_Worker_4
```
**.**  
**.**  
**.**  
On the ninth worker computer run
```shell
python3 federated_classifier.py --is_chief=False --worker_name=worker9  --file_X=X_Worker_10 --file_Y=Y_Worker_10
```

