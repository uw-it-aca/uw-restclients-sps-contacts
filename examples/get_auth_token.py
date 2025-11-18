import os


def get_auth_token():
    from uw_sps_contacts.dao import Contacts_DAO

    dao = Contacts_DAO()
    headers = dao._custom_headers('post', '', {}, '')
    print(headers)


if __name__ == '__main__':
    from commonconf.backends import use_configparser_backend
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'SPS_CONTACTS_AUTH')

    get_auth_token()
