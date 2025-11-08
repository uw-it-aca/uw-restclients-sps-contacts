# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core import models


# TODO: This may become a single contact
class EmergencyContacts(models.Model):
    syskey = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    relationship = models.CharField()
    last_modified = models.DateTimeField()  # reflects lastModified in SPS API?

    @staticmethod
    def from_json(data):
        contacts = []
        for datum in data:  # data is assumed to be a list of contact dicts
            contact = EmergencyContacts()
            contact.syskey = datum["syskey"]
            contact.name = datum["name"]
            contact.phone_number = datum["phoneNumber"]
            contact.email = datum["email"]
            contact.relationship = datum["relationship"]
            contact.last_modified = datum["lastModified"]
            contacts.append(contact)

        return contacts

    def json_data(self):
        return {
            "syskey": self.syskey,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "relationship": self.relationship,
            "last_modified": self.last_modified,  # lastModified in SPS API?
        }
