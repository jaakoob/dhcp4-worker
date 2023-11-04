# dhcp4-worker

dhcp4-worker takes DHCPv4 reservations from a message queue and configures them into kea servers.
In the message queue there can either be a full config with numerous dhcp reservations which 
get applied in total (removing all current reservations) or single items which should be removed 
or added. Ordering in the message queue plays an important role here as reservations have to be removed 
before new ones can be added for the same hw-address or IP address. 

## Getting started

```
python3 -m venv venv
pip3 install --upgrade pip
pip3 install -r requirements.txt
cp config.py.sample config.py
```

Edit the config file wih a kea ctrl agent and credentials for the message queue.

```
python3 dhcp4-worker.py
```

## Pitfalls with kea

- The kea API returns data in a strange format. Please add appropriate handling if not already present. 
- The default Kea installation on Deb 12 prevents kea from writing its own config files through apparmor. Appropriate 
permissions have to be added in the apparmor config to get things fully operational. 

## Data format in the message queue

Data in the message queue is formatted in two different ways. Either there is a single lease with the following format:

```
[
    {
        "ipv4Address": "192.0.2.1",
        "macAddress": "ff:ff:ff:ff:ff:ff",
        "operation": "(release|reserve)"
    }
]
```

Alternatively there are multiple reservations without an operation:

```
[
    {
        "ipv4Address": "192.0.2.1",
        "macAddress": "ff:ff:ff:ff:ff:ff",
    },{
        "ipv4Address": "192.0.2.2",
        "macAddress": "ff:ff:ff:ff:ff:fe",
    }
]
```