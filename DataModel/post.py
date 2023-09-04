from DataModel.reaction import Reaction, ReactionEncoder
from DataModel.author import Author, AuthorEncoder
import json
import ast


class Post:
    '''
    This class defines the post data structure
    '''

    def __init__(self, id: str, author: Author, text: str, media_url: str, reaction: Reaction, media_path: str = None):
        '''
        To init the object the information about
        :param author: the authors of the post
        :param text: the text connected to the post
        :param media_url: the url of the associated media
        :param reaction: the @Reaction datastructure
        :param media_path: the absolute path where the image is saved
        '''
        self.id = id
        self.author = author
        self.text = text
        self.media_url = media_url
        self.reaction = reaction
        self.media_path = media_path


class PostEncoder(json.JSONEncoder):
    def default(self, o: Post) -> dict:
        dictionary = {}
        for k in o.__dict__:
            if k == 'author':
                dictionary[k] = AuthorEncoder().encode(o.__dict__[k])
            if k == 'reaction':
                dictionary[k] = ast.literal_eval(ReactionEncoder().encode(o.__dict__[k]))
            else:
                dictionary[k] = o.__dict__[k]

        return dictionary
