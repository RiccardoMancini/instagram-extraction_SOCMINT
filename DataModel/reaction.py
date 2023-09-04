import json
import ast
from DataModel.comment import CommentEncoder
class Reaction:
    '''
    This class describe the reaction data strucutre
    '''

    def __init__(self, like: int, comments: list, n_comment: int):
        '''
        The init is based on the next information:
        :param like: the number of likes for the considered post
        :param comments: the list of comments based on @Comment data structure
        :param n_comment: the number of the comments for the post
        '''
        self.like_count = like
        self.n_comment = n_comment
        self.comments = comments


class ReactionEncoder(json.JSONEncoder):
    def default(self, o: Reaction) -> dict:
        dictionary = {}
        for k in o.__dict__:
            if k == 'comments':
                comments_list = []
                for comm in o.__dict__[k]:
                    comments_list.append(ast.literal_eval(CommentEncoder().encode(comm)))
                dictionary[k] = comments_list
            else:
                dictionary[k] = o.__dict__[k]
        return dictionary
