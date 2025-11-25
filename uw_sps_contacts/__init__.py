# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with the Student Contacts Web Service.
"""

import json
from uw_sps_contacts.dao import Contacts_DAO
from uw_sps_contacts.models import EmergencyContact, FamilyContact
from restclients_core.exceptions import DataFailureException
import logging


class ContactsList(object):
    def __init__(self, act_as=None):
        self.dao = Contacts_DAO()

    def _get_contacts_url(self, syskey):
        return f"/contacts/v1/emergencyContacts/{syskey}"

    def _get_resource(self, syskey, clear_cached_token=False):
        if clear_cached_token:
            self.dao.clear_access_token()
        return self.dao.getURL(
            self._get_contacts_url(syskey), {"Accept": "application/json"}
        )

    def get_contacts(self, syskey):
        response = self._get_resource(syskey)
        if response.status == 200:
            return self._process_data(json.loads(response.data))

        if response.status == 401 or response.status == 403:
            # clear token cache, retry
            response = self._get_resource(syskey, clear_cached_token=True)
            if response.status == 200:
                return self._process_data(json.loads(response.data))

        raise DataFailureException(
            self._get_contacts_url(syskey), response.status, str(response.data)
        )

    def put_list(self, eclist):
        return [
            contact.put_data() for contact in eclist if not contact.is_empty()
        ]

    def put_contacts(self, syskey, eclist):
        url = self._get_contacts_url(syskey)
        body = json.dumps(self.put_list(eclist))

        response = self._put_resource(url, body)

        if response.status == 401 or response.status == 403:
            # clear token cache, retry
            response = self._put_resource(url, body, clear_cached_token=True)
            if response.status == 200:
                return response

    def _process_data(self, jdata):
        data = []
        for i in jdata:
            em_contact = EmergencyContact(data=i)
            data.append(em_contact)

        return data

    def _put_resource(self, url, body={}, clear_cached_token=False):
        if clear_cached_token:
            self.dao.clear_access_token()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Connection": "keep-alive",
        }
        return self.dao.putURL(url, headers, body)


class FamilyContacts(object):
    def __init__(self, act_as=None):
        self.dao = Contacts_DAO()

    def _get_contact_url(self, syskey):
        return f"/student/registration/v1/address/{syskey}"

    def get_contact(self, syskey):
        response = self._get_resource(syskey)
        if response.status == 200:
            return self._process_data(json.loads(response.data))

        if response.status == 401 or response.status == 403:
            # clear token cache, retry
            response = self._get_resource(syskey, clear_cached_token=True)
            if response.status == 200:
                return self._process_data(json.loads(response.data))

        raise DataFailureException(
            self._get_contact_url(syskey), response.status, str(response.data)
        )

    def _get_resource(self, syskey, clear_cached_token=False):
        if clear_cached_token:
            self.dao.clear_access_token()
        return self.dao.getURL(
            self._get_contact_url(syskey), {"Accept": "application/json"}
        )

    def _process_data(self, jdata):
        data = FamilyContact(data=jdata)

        return data
