# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_sps_contacts import ContactsList


class ContactsListTest(TestCase):

    def test_emergency_contacts_url(self):
        contacts = ContactsList()
        self.assertEqual(
            "/contacts/v1/emergencyContacts/12345",
            contacts._get_emergency_contacts_url(12345)
        )
