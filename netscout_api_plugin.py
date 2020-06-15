import os
import re
import logging
import json
import requests
#cllects data from NetScout
from collectData import collectData
#Dynatrace Plugin SDK
from ruxit.api.base_plugin import RemoteBasePlugin
logger = logging.getLogger(__name__)

class netScoutPlugin(RemoteBasePlugin):

    #Were global variables are set in format self.{variablename} = aValue
    def initialize(self, **kwargs):
        config = kwargs['config']

        #Input from enpoint setup is made here self.{endpointKey} = self.config.get("endpointKey","DefaultValue")
        #Default value is set so if there is no input there is at least some value in them
        self.user = self.config.get("user","admin")
        self.password = self.config.get("password", "admin")
        self.hostname = self.config.get("hostname","110.1.1.1")
        self.type = self.config.get("type","Interface")


    def query(self, **kwargs):
        #Retrieves API token
        netScoutToken = collectData.authenticate(self.hostname,self.user, self.password)
        #Retrives JSON Statment
        topology = interfacePerfData(self.hostname,netScoutToken,self.type).json()

        #sample data comment above topology object before uncommenting lines below
        #topology = {"data": [{"interface": {"_id": "27395281-799b-11e8-bce0-b14fd48cc4ec","name": "ATM0/0/0","description": "somename","ifType": "Other","device": { "_id": "c2572860-7995-11e8-9c87-8b764b7e8e30","name": "Kerry-3581","ipAddress": "172.28.13.253"}},"status": {"green": 30.508474576271187,"yellow": 40.67796610169491,"orange": 28.8135593220339,"red": 0,"gray": 0,"worst": "orange","count": 59},"avgNetworkIn": 67.31627118644069,"avgNetworkOut": 60.83661016949152,"errorsTotal": 0.11864406779661017,"discardsTotalPercent": 0.09491525423728814}],"count": 67330,"start": 0,"limit": 1}

        #Go through each entry in netscout return statement
        group = self.topology_builder.create_group("NetScout Interface", "NetScout Interface")

        if self.type == "Interface":
            for group_t in topology['data']:
                device_name = group_t['interface']['name']
                device = group.create_device(device_name, device_name)
                logger.info("Topology: group name=%s, device name=%s", group.name, device.name)
                #Collect stats
                device.absolute(key='avgNetworkIn', value=group_t['avgNetworkIn'])
                device.absolute(key='avgNetworkOut', value=group_t['avgNetworkOut'])
        elif self.type == "Radio":
            logger.warning("Radio is not configured for API statements yet")

# foo = netScoutPlugin()
# foo.query()
