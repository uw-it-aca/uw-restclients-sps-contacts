# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with the Student Contacts Web Service.
"""

import json
from uw_sps_contacts.dao import Contacts_DAO
from uw_sps_contacts.models import EmergencyContact
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

    def _process_data(self, jdata):
        # TODO: Implement any necessary data transformation here.
        data = []
        for idx, i in enumerate(jdata, start=1):
            em_contact = EmergencyContact()
            em_contact.index = idx
            em_contact.syskey = i.get("syskey")
            em_contact.name = i.get("name")
            em_contact.phone = i.get("phoneNumber")
            em_contact.email = i.get("email")
            em_contact.relationship = i.get("relationship")
            em_contact.last_modified = i.get("lastModified")
            data.append(em_contact)

        return data
