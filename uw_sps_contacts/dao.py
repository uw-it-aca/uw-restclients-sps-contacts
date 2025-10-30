"""
Contains UW Student Contacts DAO implementations.
"""
from restclients_core.dao import DAO
from os.path import abspath, dirname
import os


class Contacts_DAO(DAO):

    def service_name(self):
        return 'sps_contacts'

    def service_mock_paths(self):
        path = [abspath(os.path.join(dirname(__file__), "resources"))]
        return path
