# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime

from restclients_core import models


class EmergencyContact(models.Model):
    id = models.CharField(max_length=255)  # not sure what the max actually is
    syskey = models.CharField(max_length=9)
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    relationship = models.CharField()
    last_modified = models.DateTimeField(null=True)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super().__init__(*args, **kwargs)

        self.id = data["id"]
        self.syskey = data["syskey"]
        self.name = data["name"]
        self.phone_number = data["phoneNumber"]
        self.email = data["email"]
        self.relationship = data["relationship"]
        try:
            self.last_modified = datetime.datetime.utcfromtimestamp(
                data["lastModified"]
            )
        except Exception:
            self.last_modified = None

    def is_empty(self):
        empty = (
            self.syskey == ""
            and self.name == ""
            and self.phone_number == ""
            and self.email == ""
            and self.relationship == ""
        )
        return empty

    def json_data(self):
        return {
            "id": self.id,
            "syskey": self.syskey,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "relationship": self.relationship,
            "last_modified": (
                self.last_modified.isoformat()
                if (self.last_modified is not None)
                else None
            ),
        }

    def put_data(self):
        return {
            "syskey": self.syskey,
            "name": self.name,
            "phoneNumber": self.phone_number,
            "email": self.email,
            "relationship": self.relationship,
        }


class FamilyContact(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super().__init__(*args, **kwargs)

        self.name = kwargs["data"]["parent_name"]
        self.phone_number = (
            kwargs["data"]["parent_address"]["phone_area"]
            + kwargs["data"]["parent_address"]["phone_prefix"]
            + kwargs["data"]["parent_address"]["phone_suffix"]
        )

    def json_data(self):
        return {
            "name": self.name,
            "phone_number": self.phone_number,
        }
