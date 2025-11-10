# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_sps_contacts.dao import Contacts_Auth_DAO


class TestSpsAuth(TestCase):

    def test_is_cacheable(self):
        auth = Contacts_Auth_DAO()
        self.assertTrue(auth._is_cacheable("POST", "/", {}, ""))
