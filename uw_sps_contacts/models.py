# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core import models
import datetime


class EmergencyContact(models.Model):
    id = models.CharField(max_length=255)  # not sure what the max actually is
    syskey = models.CharField(max_length=9)
    name = models.CharField(max_length=150)
    phoneNumber = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    relationship = models.CharField()
    lastModified = models.DateTimeField(null=True)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super().__init__(*args, **kwargs)

        self.id = data["id"]
        self.syskey = data["syskey"]
        self.name = data["name"]
        self.phoneNumber = data["phoneNumber"]
        self.email = data["email"]
        self.relationship = data["relationship"]
        try:
            self.lastModified = datetime.datetime.utcfromtimestamp(
                data["lastModified"]
            )
        except Exception:
            self.lastModified = None

    def is_empty(self):
        empty = (
            self.syskey == ""
            and self.name == ""
            and self.phoneNumber == ""
            and self.email == ""
            and self.relationship == ""
        )
        return empty

    def json_data(self):
        return {
            "id": self.id,
            "syskey": self.syskey,
            "name": self.name,
            "phoneNumber": self.phoneNumber,
            "email": self.email,
            "relationship": self.relationship,
            "lastModified": (
                self.lastModified.isoformat()
                if (self.lastModified is not None)
                else None
            ),
        }

    def put_data(self):
        return {
            "syskey": self.syskey,
            "name": self.name,
            "phoneNumber": self.phoneNumber,
            "email": self.email,
            "relationship": self.relationship,
        }


class FamilyContact(models.Model):
    name = models.CharField()
    phoneNumber = models.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super().__init__(*args, **kwargs)

        self.name = kwargs["data"]["parent_name"]
        self.phoneNumber = (
            kwargs["data"]["parent_address"]["phone_area"]
            + kwargs["data"]["parent_address"]["phone_prefix"]
            + kwargs["data"]["parent_address"]["phone_suffix"]
        )

    def json_data(self):
        return {
            "name": self.name,
            "phoneNumber": self.phoneNumber,
        }
