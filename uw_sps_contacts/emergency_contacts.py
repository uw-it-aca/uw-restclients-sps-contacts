"""
This is the interface for interacting with the Student Contacts Web Service.
"""

import logging
from uw_sps_contacts.models import EmergencyContacts

EMERGENCY_CONTACTS_URL = "/contacts/v1/emergencyContacts/{syskey}"
logger = logging.getLogger(__name__)


def get_emergency_contacts(syskey, act_as=None):
    """
    Return ...
    """
    url = EMERGENCY_CONTACTS_URL.format(syskey=syskey)
    headers = {}

    if act_as is not None:
        headers["X-UW-Act-as"] = act_as

    response = get_resource(url, headers)
    return EmergencyContacts.from_json(url, response)
