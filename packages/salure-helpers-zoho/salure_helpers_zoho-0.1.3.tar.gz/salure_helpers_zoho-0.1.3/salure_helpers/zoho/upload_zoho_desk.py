import os
import sys
import pandas as pd
from typing import Union, List
import requests
import json
from salure_helpers.salureconnect import SalureConnect

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)


class UploadZohoDesk(SalureConnect):

    def __init__(self, label: Union[str, List], debug: bool = False):
        """
        For the full documentation, see: https://avisi-apps.gitbook.io/tracket/api/
        """
        super().__init__()
        self.headers = self.__get_headers(label=label)
        self.base_url = "https://desk.zoho.com/api/v1/"

    def __get_headers(self, label):
        """
        Get the credentials for the Traket API from SalureConnect, with those credentials, get the access_token for Tracket.
        Return the headers with the access_token.
        """
        # Get credentials from SalureConnect
        credentials = self.get_system_credential(system='zoho-desk', label=label)

        # With those credentials, get the access_token from Tracket
        org_id = credentials["config"]["organisation_id"]
        zoho_system_id = credentials["id"]
        token = SalureConnect().refresh_system_credential(system="zoho-desk", system_id=zoho_system_id)["access_token"]
        headers = {
            'Authorization': f'Zoho-oauthtoken {token}',
            'orgId': f'{org_id}',
            'Content-Type': 'application/json'
        }
        return headers

    def update_ticket_time_entry(self, ticket_id, time_entry_id, payload):
        """
        This function updates the time entry of a ticket in zoho desk
        :param ticket_id: str
        :param time_entry_id: str
        :param payload: dict
        """
        url = f"{self.base_url}tickets/{ticket_id}/timeEntry/{time_entry_id}"
        response = requests.request("PATCH", url, headers=self.headers, data=json.dumps(payload))
        return response
