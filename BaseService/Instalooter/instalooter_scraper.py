import logging
from typing import Union
import time, random
import requests
from DataModel import post, comment, reaction, author
from instalooter.looters import ProfileLooter, HashtagLooter
from instalooter._utils import get_shared_data


# TODO gestire post per un determinato periodo temporale
# TODO aggiungere commenti ai metodi
class InstalooterScraper:
    """
    This is a common class that define login and scraped data results
    used by Profile and Hashtag class using Instalooter
    """

    def __init__(self, username: str, password: str):
        """
        To init the object the information about
        :param username: the username used for login
        :param password: the password used for login
        """
        self.__logger__()
        self.logger.info('Instalooter scraper init')
        self.username = username
        self.password = password

    def check_log(self, actual_looter: Union[ProfileLooter, HashtagLooter]):
        if not actual_looter.logged_in():
            actual_looter.login(self.username, self.password)
        else:
            actual_looter.logout()
            actual_looter.login(self.username, self.password)
        return actual_looter.session

    @staticmethod
    def get_author_info(usr: str, session: requests.Session) -> author.Author:
        time.sleep(min(random.expovariate(0.6), 15.0))
        url = "https://www.instagram.com/{}/feed/".format(usr)
        try:
            with session.get(url) as res:
                author_data = get_shared_data(res.text)['entry_data']['ProfilePage'][0]['graphql']['user']
        except (ValueError, AttributeError):
            raise ValueError("user not found: '{}'".format(usr))

        return author.Author(author_data['id'],
                             usr,
                             author_data['full_name'],
                             author_data['edge_followed_by']['count'],
                             author_data['edge_follow']['count'],
                             author_data['edge_owner_to_timeline_media']['count'])

    def post_results(self, post_info: dict, session: requests.Session) -> post.Post:
        author_info = self.get_author_info(post_info['owner']['username'], session)
        post_text = (post_info['edge_media_to_caption']['edges'][0]['node']['text']
                     if len(post_info['edge_media_to_caption']['edges']) != 0
                     else 'Nessuna descrizione!')
        if post_info.get('__typename') == "GraphSidecar":
            nodes = [e['node'] for e in post_info['edge_sidecar_to_children']['edges']]
            post_media = [n.get('video_url') or n.get('display_url') for n in nodes]
        elif post_info['is_video']:
            post_media = post_info['video_url']
        else:
            post_media = post_info['display_url']

        comment_list = []
        if post_info['edge_media_to_parent_comment']['count'] != 0:
            comments = [cmt['node'] for cmt in post_info['edge_media_to_parent_comment']['edges']]
            for cmt in comments:
                cmt_author_info = self.get_author_info(cmt['owner']['username'], session)
                comment_list.append(comment.Comment(cmt['id'], cmt_author_info, cmt['text']))
                if cmt['edge_threaded_comments']['count'] != 0:
                    answer_comments = [ans_cmt['node'] for ans_cmt in cmt['edge_threaded_comments']['edges']]
                    for ans_cmt in answer_comments:
                        ans_cmt_author_info = self.get_author_info(ans_cmt['owner']['username'], session)
                        comment_list.append(
                            comment.Comment(ans_cmt['id'], ans_cmt_author_info, ans_cmt['text'], True, cmt['id']))
        else:
            comment_list.append('Nessun commento in questo post!')

        return post.Post(post_info['shortcode'],
                         author_info,
                         post_text,
                         post_media,
                         reaction.Reaction(post_info['edge_media_preview_like']['count'],
                                           comment_list,
                                           post_info['edge_media_to_parent_comment']['count']))

    def __logger__(self):
        # Logging configuration
        # Create logger for Instagram Service
        self.logger = logging.getLogger('SOCMINT.InstalooterBaseService')
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
