from restclients_core import models


# TODO: This may become a single contact
class EmergencyContacts(models.Model):
    syskey = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    relationship = models.CharField()
    last_modified = DateTimeField()  # reflects lastModified in SPS API?

    def from_json(data):
        contact = EmergencyContacts()
        for datum in data[0]:  # TODO: how to handle the list of contacts?
            contact.syskey = datum['syskey']
            contact.name = datum['name']
            contact.phone_number = datum['phoneNumber']
            contact.email = datum['email']
            contact.relationship = datum['relationship']
            contact.last_modified = datum['lastModified']

        return contact

    def json_data(self):
        return {
            "syskey": self.syskey,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "relationship": self.relationship,
            "last_modified": self.last_modified,  # lastModified in SPS API?
        }
