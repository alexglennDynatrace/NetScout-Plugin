import os
import requests
from requests import exceptions
import logging
import json
import sys

logger = logging.getLogger(__name__)
class collectData:
    #Establish connection with NetScout
    def authenticate(hostname, username, password):
        url ='https://' +  hostname + '/ngp/v2/login'
        #Disable the SSL warning when using the default cert or unsigned cert using the disable_warnings function.
        #Follow up with verify=False in the requests.
        #Do yourself a favor and get a signed cert for proper security
        #gets all unique names for PC
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        try:
            resp = requests.request("POST",url,json={'emailOrUsername': username, 'password' : password}, verify=False)
            resp.raise_for_status()
        except requests.packages.RequestException as err:
            logger.warning(err)
            sys.exit()
        token = json.loads(resp.content)["accessToken"]
        return token

    def interfacePerfData(hostname,token):
        url = hostname + '/ngp/v2/interfaces/perf'
        try:
            resp = requests.request("GET",url, headers={'ngp-authorization': 'Access '+token},verify=False)
            resp.raise_for_status()
        except requests.packages.RequestException as err:
            logger.warning(err)
            sys.exit()
        return resp
if __name__ == '__main__':
    collectData()
