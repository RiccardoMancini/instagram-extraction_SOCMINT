import json
class Author:
    '''
    This class represent the author of the post on the social
    '''
    def __init__(self, id, username: str, name: str, follower: int, following: int, n_posts: int, platform: str = 'Instagram'):
        '''
        The class describe an author for a post
        :param username: the username of the author
        :param name: the complite name of the author
        :param follower: the number of follower of the author (the friends for facebook)
        :param following: the number of following of the author
        :param n_posts: the number of posts pubblished
        :param platform: the plaform of the author
        '''
        self.id = id
        self.username = username
        self.name = name
        self.follower = follower
        self.following = following
        self.n_posts = n_posts
        self.platform = platform

class AuthorEncoder(json.JSONEncoder):
    def default(self, o: Author) -> dict:
        dictionary = {}
        for k in o.__dict__:
            dictionary[k] = o.__dict__[k]
        return dictionary