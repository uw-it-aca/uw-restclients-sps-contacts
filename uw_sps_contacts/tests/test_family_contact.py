# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import mock
from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from restclients_core.models import MockHTTP
from uw_sps_contacts import FamilyContacts


class FamilyContactsTest(TestCase):

    def test_family_contact_url(self):
        contact = FamilyContacts()
        self.assertEqual(
            "/student/registration/v1/address/12345",
            contact._get_contact_url(12345),
        )

    @mock.patch.object(FamilyContacts, "_get_resource")
    def test_error_401(self, mock):
        response = MockHTTP()
        response.status = 401
        response.data = "Not Authorized"
        mock.return_value = response
        with self.assertRaises(DataFailureException):
            FamilyContacts().get_contact(12345)

    def test_family_contact_javerage(self):
        fcontacts = FamilyContacts()
        contact = fcontacts.get_contact(12345)

        self.assertEqual('NAME,PARENT', contact.name)
        self.assertEqual('2064444444', contact.phone_number)

        resp = fcontacts._get_resource(12345, clear_cached_token=True)
        self.assertIsNotNone(resp)

    def test_json_data(self):
        pass
