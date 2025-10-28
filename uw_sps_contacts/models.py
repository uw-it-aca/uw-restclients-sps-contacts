from restclients_core import models


# TODO: This may become a single contact
class EmergencyContacts(models.Model):
    syskey = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    relationship = (
        models.PositiveSmallIntegerField()
    )  # looks like it needs has_choices=True
    last_modified = DateTimeField()  # reflects lastModified in SPS API?

    def json_data(self):
        return {
            "syskey": self.syskey,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "relationship": self.relationship,
            "last_modified": self.last_modified,  # lastModified in SPS API?
        }
