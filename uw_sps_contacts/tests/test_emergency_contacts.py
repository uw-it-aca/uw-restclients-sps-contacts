# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
import mock
from restclients_core.models import MockHTTP
from restclients_core.exceptions import DataFailureException
from uw_sps_contacts import ContactsList


class ContactsListTest(TestCase):

    def test_emergency_contacts_url(self):
        contacts = ContactsList()
        self.assertEqual(
            "/contacts/v1/emergencyContacts/12345",
            contacts._get_contacts_url(12345)
        )

    @mock.patch.object(ContactsList, "_get_resource")
    def test_error_401(self, mock):
        response = MockHTTP()
        response.status = 401
        response.data = "Not Authorized"
        mock.return_value = response
        with self.assertRaises(DataFailureException):
            ContactsList().get_contacts(12345)

    def test_contacts_for_javerage(self):
        contactslist = ContactsList()
        contacts = contactslist.get_contacts(12345)
        self.assertEqual(len(contacts), 1)
