# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core import models
import datetime


class EmergencyContact(models.Model):
    syskey = models.CharField(max_length=9)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    relationship = models.CharField()
    last_modified = models.DateTimeField(null=True)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super().__init__(*args, **kwargs)

        self.syskey = data["syskey"]
        self.name = data["name"]
        self.phone = data["phoneNumber"]
        self.email = data["email"]
        self.relationship = data["relationship"]
        try:
            self.last_modified = datetime.datetime.utcfromtimestamp(
                data["lastModified"]
            )
        except Exception:
            self.last_modified = None

    def json_data(self):
        return {
            "syskey": self.syskey,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "relationship": self.relationship,
            "last_modified": (
                self.last_modified.isoformat()
                if (self.last_modified is not None)
                else None
            ),
        }
