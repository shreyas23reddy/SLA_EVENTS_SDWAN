# SLA_EVENTS_SDWAN



# vManage APIs for SLA CHANGE EVENT ALERTS

This public repo contains python code that can be used to interact with the `Cisco SD-WAN vManage REST API`. Tested the code on on-prem lab running 20.5.x.You can edit the variables in the environment to point to your own vManage instance. The code contains REST API calls to authenticate, get a list of devices that are part of the SD-WAN fabric. 



# Objective 

*   How to use vManage APIs - 
    - This is indented to send SLA Changes Events to email from vmanage 
    - Program runs in a loop with a delay of 3 mins for each run.
    

# Requirements

To use this code you will need:

* Python 3.7+
* vManage user login details. (User should have privilege level to configure policies)

# Install and Setup

- Clone the code to local machine.

```
git clone https://github.com/shreyas23reddy/SLA_EVENTS_SDWAN.git
cd sdwan-app-route-policy
```
- Setup Python Virtual Environment (requires Python 3.7+)

```
python3.7 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

- A YAML file with the Cisco SD-WAN Sandbox has been created **vmanage_login.yaml** You can edit the variables in the environment to point to your own vManage instance.



USE events_SLA.py to run the code 
