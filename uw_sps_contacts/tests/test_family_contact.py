# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import mock
from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from restclients_core.models import MockHTTP
from uw_sps_contacts import FamilyContact


class FamilyContactTest(TestCase):

    def test_family_contact_url(self):
        contact = FamilyContact()
        self.assertEqual(
            "/registration/v1/address/12345",
            contact._get_contact_url(12345),
        )

    @mock.patch.object(FamilyContact, "_get_resource")
    def test_error_401(self, mock):
        response = MockHTTP()
        response.status = 401
        response.data = "Not Authorized"
        mock.return_value = response
        with self.assertRaises(DataFailureException):
            FamilyContact().get_contact(12345)
