import json
class User:
    '''
    This class define the User data representation
    A user is a SOCMINT user
    With User it is possible to get the settings associated with it like analysis and scraping limits
    '''
    def __init__(self, id: str, username: str, settings: dict):
        '''
        The init funcion require the username and the settings
        :param username: the user name of user
        :param settings: the settings associated with the user
        '''
        self.id = id
        self.username = username
        self.settings = settings

    def get_settings(self):
        return self.settings

class UserEncoder(json.JSONEncoder):
    def default(self, o: User) -> dict:
        dictionary = {}
        for k in o.__dict__:
            dictionary[k] = o.__dict__[k]
        return dictionary