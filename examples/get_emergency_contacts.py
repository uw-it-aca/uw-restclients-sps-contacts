from commonconf.backends import use_configparser_backend
from commonconf import settings
import os
from uw_sps_contacts import ContactsList
#from requests_oauthlib import OAuth2Session

#settings.configure()

#client_id = getattr(settings, 'SPS_CONTACTS_CLIENT_ID')
#client_secret = getattr(settings, 'SPS_CONTACTS_CLIENT_SECRET')

#def get_token():
#    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
#                                'settings.cfg')
#    use_configparser_backend(settings_path, 'SPS_CONTACTS')
#    access_token = get_resource(f"/oauth2/token")
#    print(access_token)


def get_contacts(syskey):
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                'settings.cfg')
    use_configparser_backend(settings_path, 'SPS_CONTACTS')
    #import pdb; pdb.set_trace()
    #contacts = ContactsList().get_contacts(syskey)
    contacts_instance = ContactsList()
    contacts = contacts_instance.get_contacts(syskey)

    print(contacts)


#def get_oauth2_session():
#    # Create a client for client credentials flow
#    client = BackendApplicationClient(client_id=client_id)
#    oauth = OAuth2Session(client=client)
#    return oauth


if __name__ == "__main__":
    get_contacts(00000)
    #get_oauth2_sesssion()
    #get_token()
