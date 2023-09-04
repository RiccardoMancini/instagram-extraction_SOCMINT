import json

class Campaign:
    '''
    This class represent the Campaign data inside the db
    '''
    def __init__(self, id: str, name: str, trackers: list, limit: int):
        '''
        The initialization uses:
        :param id: a string that is the unique ID
        :param name: a string that define the name of the campaign
        :param trackers: the list of trackers
        :param limit: the limitof number of post associated to this campaign
        '''
        self.id = id
        self.name = name
        self.trackers = trackers
        self.limit = limit

class CampaignEncoder(json.JSONEncoder):
    def default(self, o: Campaign) -> dict:
        dictionary = {}
        for k in o.__dict__:
            dictionary[k] = o.__dict__[k]

        return dictionary