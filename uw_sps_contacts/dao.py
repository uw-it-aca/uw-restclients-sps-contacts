"""
Contains UW Student Contacts DAO implementations.
"""
import json
import logging
import os
from os.path import abspath, dirname
from restclients_core.dao import DAO
from restclients_core.exceptions import DataFailureException

logger = logging.getLogger(__name__)
sps_contacts_access_token_url = "/oauth2/token"


class Contacts_Auth_DAO(DAO):
    def service_name(self):
        return 'sps_contacts_auth'

    def _is_cacheable(self, method, url, headers, body=None):
        return True

    def clear_token_from_cache(self):
        self.clear_cached_response(sps_contacts_access_token_url)

    def get_auth_token(self, secret):
        headers = {"Authorization": "Basic {}".format(secret),
                   "Content-type": "application/x-www-form-urlencoded"}

        response = self.postURL(
            sps_contacts_access_token_url, headers, "grant_type=client-credentials")
        if response.status != 200:
            logger.error({'url': sps_contacts_access_token_url,
                          'status': response.status,
                          'data': response.data})
            raise DataFailureException(
                sps_contacts_access_token_url, response.status, response.data)

        data = json.loads(response.data)
        return data.get("access_token", "")

    def service_mock_paths(self):
        path = [abspath(os.path.join(dirname(__file__), "resources"))]
        return path

    def _edit_mock_response():
        pass  # need to implement? check myplan dao


class Contacts_DAO(DAO):
    def __init__(self):
        self.auth_dao = Contacts_Auth_DAO()
        return super(Contacts_DAO, self).__init__()

    def service_name(self):
        return 'sps_contacts'

    def service_mock_paths(self):
        path = [abspath(os.path.join(dirname(__file__), "resources"))]
        return path

    def _custom_headers(self, method, url, headers, body):
        if not headers:
            headers = {}
        secret = self.get_service_setting("AUTH_SECRET", "")
        if secret:
            token = self.auth_dao.get_auth_token(secret)
            headers["Authorization"] = f"Bearer {token}"
        return headers
