# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_sps_contacts.dao import Contacts_Auth_DAO
from uw_sps_contacts.utils import (
    fdao_sps_contacts_override, fdao_sps_contacts_auth_override)


@fdao_sps_contacts_auth_override
@fdao_sps_contacts_override
class TestSpsAuth(TestCase):

    def test_is_cacheable(self):
        auth = Contacts_Auth_DAO()
        self.assertTrue(auth._is_cacheable("POST", "/", {}, ""))

    def test_get_auth_token(self):
        self.assertIsNotNone(
            Contacts_Auth_DAO().get_auth_token("test1"))
