# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import mock
import datetime
from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from restclients_core.models import MockHTTP
from uw_sps_contacts import ContactsList
from uw_sps_contacts.models import EmergencyContact


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

        self.assertEqual(type([]), type(contacts))

        self.assertEqual(
            "ab269f37-2807-4b10-b9d3-b5f7c602d45f", contacts[0].id
        )
        self.assertEqual(12345, contacts[0].syskey)
        self.assertEqual("John Doe", contacts[0].name)
        self.assertEqual("5551234567", contacts[0].phoneNumber)
        self.assertEqual("foo@example.com", contacts[0].email)
        self.assertEqual("PARENT", contacts[0].relationship)
        self.assertEqual(
            datetime.datetime(2025, 11, 11, 21, 28, 40, 180882),
            contacts[0].lastModified,
        )

        self.assertEqual(
            "eacccecd-8db7-48b7-8b0b-ff5d87e379f5", contacts[1].id
        )
        self.assertEqual(12345, contacts[1].syskey)
        self.assertEqual("Jane Doe", contacts[1].name)
        self.assertEqual("5557654321", contacts[1].phoneNumber)
        self.assertEqual("bar@example.com", contacts[1].email)
        self.assertEqual("PARENT", contacts[1].relationship)
        self.assertEqual(
            datetime.datetime(2025, 11, 11, 21, 28, 40, 267776),
            contacts[1].lastModified,
        )

        resp = contactslist._get_resource(12345, clear_cached_token=True)
        self.assertIsNotNone(resp)

    def test_json_data(self):
        contact = EmergencyContact()
        contact.id = "totally-fake-id-1"
        contact.syskey = 0
        contact.name = "Jeremiah Doe"
        contact.phoneNumber = "+442079460000"
        contact.email = "oof@example.com"
        contact.relationship = "SIBLING"

        self.assertIsInstance(contact.json_data(), dict)
        string_data = (
            '{"id": "totally-fake-id-1", '
            '"syskey": 0, '
            '"name": "Jeremiah Doe", '
            '"phoneNumber": "+442079460000", '
            '"email": "oof@example.com", '
            '"relationship": "SIBLING", '
            '"lastModified": null}'
        )
        self.assertEqual(contact.json_data(), json.loads(string_data))

    @mock.patch.object(ContactsList, "_put_resource")
    def test_update_contacts(self, mock_update):
        mock_update.return_value = None
        eclist = []
        string_data = (
            '{"id": "totally-fake-id-2", '
            '"syskey": 12345, '
            '"name": "Jupiter Doe", '
            '"phoneNumber": "+442079460000", '
            '"email": "oof@example.com", '
            '"relationship": "SIBLING", '
            '"lastModified": null}'
        )
        ec1 = EmergencyContact(data=json.loads(string_data))
        ec2 = EmergencyContact()
        eclist.append(ec1)
        eclist.append(ec2)
        contactslist = ContactsList()
        contactslist.put_contacts(12345, eclist)

        mock_update.assert_called_with(
            "/contacts/v1/emergencyContacts/12345",
            json.dumps(contactslist.put_data(eclist)),
        )

    def test_empty_contact(self):
        string_data = (
            '{"id": "totally-fake-id-2", '
            '"syskey": 12345, '
            '"name": "Jupiter Doe", '
            '"phoneNumber": "+442079460000", '
            '"email": "oof@example.com", '
            '"relationship": "SIBLING", '
            '"lastModified": null}'
        )
        ec1 = EmergencyContact(data=json.loads(string_data))
        self.assertFalse(ec1.is_empty())
        ec2 = EmergencyContact()
        self.assertTrue(ec2.is_empty())
