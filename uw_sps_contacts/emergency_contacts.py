"""
This is the interface for interacting with the Student Contacts Web Service.
"""

import logging
import simplejson as json
from uw_sps_contacts.models import EmergencyContacts
from uw_sps_contacts import get_resource
from restclients_core.exceptions import DataFailureException

url_prefix = "/contacts/v1/emergencyContacts/"
logger = logging.getLogger(__name__)


def get_emergency_contacts(syskey, act_as=None):
    """
    Return ...
    """
    url = "%s%s" % syskey
    headers = {}

    if act_as is not None:
        headers["X-UW-Act-as"] = act_as

    response = get_resource(url, headers)
    return _object_from_json(url, reponse)


def _object_from_json(url, response_body):
    json_data = json.loads(response_body)
    return_obj = EmergencyContacts()

    ec_data = json_data.get()
    if ec_data is None:
        raise DataFailureException(url, 500, "error: bad resposne data")

    try:
        return "Implement me"
    except Exception as ex:
        logger.debug("Exception: %s" % ex)
