import json
from DataModel.author import Author, AuthorEncoder
import ast


class Comment():
    '''
    This class define the data strucutre of a comment for the post
    '''

    def __init__(self, id: str, author: Author, text: str, answer: bool = False, id_comment: str = None):
        '''
        The object creation is based on the next information:
        :param author: is an author of the posts
        :param text: the text inside a comment
        '''
        self.id = id
        self.author = author
        self.text = text
        self.answer = answer
        self.id_comment = id_comment


class CommentEncoder(json.JSONEncoder):
    def default(self, o: Comment) -> dict:
        dictionary = {}
        for k in o.__dict__:
            if k == 'author':
                dictionary[k] = ast.literal_eval(AuthorEncoder().encode(o.__dict__[k]))
            elif k == 'answer':
                dictionary[k] = str(o.__dict__[k])
            elif k == 'id_comment' and o.__dict__[k] == None:
                dictionary[k] = 'none'
            else:
                dictionary[k] = o.__dict__[k]
        return dictionary
