import json


class TrackerSettings:
    '''
    This class represent the settings of a tracker that permit us to check a trecker settings
    '''
    def __init__(self, facebook: dict, twitter: dict, instagram: dict):
        '''
        The initialization require
        :param facebook: a dictionary with the activated or not platform and the limit of the number of posts associated to the platform
        :param twitter: a dictionary with the activated or not platform and the limit of the number of posts associated to the platform
        :param instagram: a dictionary with the activated or not platform and the limit of the number of posts associated to the platform
        '''
        self.facebook = facebook

        self.instagram = instagram

        self.twitter = twitter


class TrackerSettingsEncoder(json.JSONEncoder):
    def default(self, o: TrackerSettings) -> dict:
        dictionary = {}
        for k in o.__dict__:
            dictionary[k] = {}
            for key in o.__dict__[k]:
                if type(o.__dict__[k][key]) == bool:
                    dictionary[k][key] = str(o.__dict__[k][key])
                else:
                    dictionary[k][key] = o.__dict__[k][key]
        return dictionary