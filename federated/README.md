### Prerequisites

- Install Iroha python sdk
```
pip install iroha
```
### Create a domain, asset and default role in the BSMD network
```
python3 setup.py
```
The setup.py file create a the domain **federated**, an asset call **fedcoin** and a default role call **user**. Domains are use to grup a set of users with common goals. For example, in this case all nodes will use the BSMD for participating in a Federated Learning algorothm, hence all nodes must be in the domain **federated**. A node can be part of different domains. 

**Assets** are virtual coins the **users** use for payments


