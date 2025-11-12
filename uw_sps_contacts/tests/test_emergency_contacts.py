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
            contacts._get_contacts_url(12345),
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
        self.assertEqual(len(contacts), 2)

        # should be a list of models
        self.assertEqual(type([]), type(contacts))
        self.assertEqual(12345, contacts[0].syskey)
        self.assertEqual("John Doe", contacts[0].name)
        self.assertEqual("5551234567", contacts[0].phone)
        self.assertEqual("foo@example.com", contacts[0].email)
        self.assertEqual("PARENT", contacts[0].relationship)
        # last_modified assertion here

        self.assertEqual(12345, contacts[1].syskey)
        self.assertEqual("Jane Doe", contacts[1].name)
        self.assertEqual("5557654321", contacts[1].phone)
        self.assertEqual("bar@example.com", contacts[1].email)
        self.assertEqual("PARENT", contacts[1].relationship)
        # last_modified assertion here

        resp = contactslist._get_resource(12345, clear_cached_token=True)
        self.assertIsNotNone(resp)

    def test_json(self):
        contactslist = ContactsList()
        contacts = contactslist.get_contacts(12345)
