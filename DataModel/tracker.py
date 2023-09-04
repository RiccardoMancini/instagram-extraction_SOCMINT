import ast
import json
from DataModel.tracker_settings import TrackerSettings, TrackerSettingsEncoder


class Tracker:
    '''
    This class represent a tracker from Database that can be used to check tracker settings
    '''

    def __init__(self, id: str, settings: TrackerSettings, hashtag: dict, creator: dict, page: dict):
        '''
        The initialization of the tracker require
        :param id: a string that is the unique ID of the databases
        :param settings: a settings object
        :param hashtag: a dictionary that contains the hashtags separated by platform and the number of posts associated to it
        :param creator: a dictionary that contains the hashtags separated by platform and the number of posts associated to it
        :param page: a dictionary that contains the hashtags separated by platform and the number of posts associated to it
        '''
        self.id = id
        self.settings = settings
        self.hashtag = hashtag
        self.creator = creator
        self.page = page


class TrackerEncoder(json.JSONEncoder):
    def default(self, o: Tracker) -> dict:
        dictionary = {}
        for k in o.__dict__:
            if k == 'settings':
                dictionary[k] = ast.literal_eval(TrackerSettingsEncoder().encode(o.__dict__[k]))
            else:
                dictionary[k] = o.__dict__[k]
        return dictionary