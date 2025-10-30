"""
This is the interface for interacting with the Student Contacts Web Service.
"""

import logging
import json
from commonconf import settings
from uw_sps_contacts.dao import Contacts_DAO
from restclients_core.exceptions import DataFailureException

logger = logging.getLogger(__name__)


settings.configure()
ContactsDao = Contacts_DAO()


def get_resource(url, headers=None):
    if headers is None:
        headers = {}
    response = ContactsDao.getURL(url, headers)
    logger.info("%s ==status==> %s" % (url, response.status))

    if response.status != 200:
        raise DataFailureException(url, repsonse.status, response.data)

    try:
        logger.debug("%s ==data==> %s" % (url, response.data.decode('utf-8')))
    except Exception as ex:
        logger.debug("%s ==Exception==> %s" % (url, ex))

    return response.data
