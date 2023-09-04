import logging
from instaloader import Instaloader, Post
from datetime import datetime
from DataModel import post, comment, reaction, author


# TODO gestire post per un determinato periodo temporale
# TODO aggiungere commenti ai metodi
class InstaloaderScraper:
    """
    This is a common class that define login and scraped data results
    used by Profile and Hashtag with Instaloader
    """

    def __init__(self, username: str, password: str,
                 since: datetime = None, until: datetime = None):
        """
        To init the object the information about
        :param ist: Instaloader() istance
        :param username: the username used for login
        :param password: the password used for login
        :param since: time limit from which to scrape data
        :param until: time limit not to be exceeded to scrape data
        """
        self.__logger__()
        self.logger.info('Instaloader scraper init')
        self.ist = Instaloader()
        self.username = username
        self.password = password
        self.since = since if since is not None else datetime.min
        self.until = until if until is not None else datetime.now()

    def check_log(self):
        self.ist.login(self.username, self.password)

    @staticmethod
    def post_results(pst: Post) -> post.Post:
        post_text = (pst._node['edge_media_to_caption']['edges'][0]['node']['text']
                     if len(pst._node['edge_media_to_caption']['edges']) != 0
                     else 'Nessuna descrizione!')
        if pst.typename == 'GraphSidecar':
            nodes = [e for e in pst.get_sidecar_nodes()]
            post_media = [n[1] if not n[0] else n[2] for n in nodes]
        elif pst.is_video:
            post_media = pst._node['video_url']
        else:
            post_media = pst._node['display_url']

        comment_list = []
        if pst.comments != 0:
            comments = pst.get_comments()
            for cmt in comments:
                comment_author = author.Author(cmt[3].userid, cmt[3].username, cmt[3].full_name,
                                               cmt[3].followers, cmt[3].followees, cmt[3].mediacount)
                comment_list.append(comment.Comment(str(cmt[0]), comment_author, cmt[2]))

                for cmt_answer in cmt[5]:
                    comment_answer_author = author.Author(cmt_answer[3].userid, cmt_answer[3].username,
                                                          cmt_answer[3].full_name,
                                                          cmt_answer[3].followers, cmt_answer[3].followees,
                                                          cmt_answer[3].mediacount)
                    comment_list.append(
                        comment.Comment(str(cmt_answer[0]), comment_answer_author, cmt_answer[2], True, cmt[0]))
        else:
            comment_list.append('Nessun commento in questo post!')

        return post.Post(pst.shortcode,
                         author.Author(pst.owner_id, pst.owner_username, pst.owner_profile.full_name,
                                       pst.owner_profile.followers, pst.owner_profile.followees,
                                       pst.owner_profile.mediacount),
                         post_text,
                         post_media,
                         reaction.Reaction(sum(1 for _ in pst.get_likes()), comment_list, pst.comments))

    def __logger__(self):
        # Logging configuration
        # Create logger for Instagram Service
        self.logger = logging.getLogger('SOCMINT.InstaloaderBaseService')
        self.logger.setLevel(logging.DEBUG)
        # File handler logger
        fh = logging.FileHandler('./logging/BaseService.log')
        fh.setLevel(logging.DEBUG)
        # Console handler logger
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # logging formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add handler to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
