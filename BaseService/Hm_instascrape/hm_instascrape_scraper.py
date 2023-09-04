import logging
import urllib.parse
import json
import random
import re
#from instascrape.scrapers import Profile as Profile_instascrape, Hashtag as Hashtag_instascrape
from datetime import datetime
import time
import lxml.html
import requests
from DataModel import author, comment, post, reaction


class HmInstaScrapeScraper:

    def __init__(self, username: str, password: str):
        self.__logger__()
        self.logger.info('Hm_instascrape scraper init')
        self.username = username
        self.password = password
        self.url = 'https://www.instagram.com/accounts/login/'
        self.url_login = 'https://www.instagram.com/accounts/login/ajax/'
        self.user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"

    def get_insta_session(self):
        def get_csrf_token(content: requests.Response):
            xpath_data = lxml.html.fromstring(content).xpath('/html/body/script[1]/text()')[0]
            raw_json = xpath_data[xpath_data.find('{'):-1]
            return json.loads(raw_json)["config"]["csrf_token"]

        time_req = int(datetime.now().timestamp())
        response = requests.get(self.url, headers={
            'User-agent': self.user_agent
        })
        csrf = get_csrf_token(response.content)
        payload = {
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time_req}:{self.password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        login_header = {
            "User-Agent": self.user_agent,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        }

        login_response = requests.post(self.url_login, data=payload, headers=login_header)
        json_data = json.loads(login_response.text)
        if json_data["authenticated"]:
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            session_utils = {
                "csrf_token": cookie_jar['csrftoken'],
                "session_id": cookie_jar['sessionid']
            }

            return session_utils

    @staticmethod
    def get_shared_data(html):
        match = re.search(r'window._sharedData = ({[^\n]*});', html)
        return json.loads(match.group(1))

    def get_author_info(self, usr: str) -> author.Author:
        time.sleep(min(random.expovariate(0.6), 15.0))
        url = "https://www.instagram.com/{}/feed/".format(usr)
        try:
            with requests.get(url, headers={
                'User-agent': self.user_agent
            }) as res:
                author_data = self.get_shared_data(res.text)['entry_data']['ProfilePage'][0]['graphql']['user']
        except (ValueError, AttributeError):
            raise ValueError("user not found: '{}'".format(usr))

        return author.Author(author_data['id'],
                             usr,
                             author_data['full_name'],
                             author_data['edge_followed_by']['count'],
                             author_data['edge_follow']['count'],
                             author_data['edge_owner_to_timeline_media']['count'])

    def get_profile_posts(self, usr: str, headers: dict):
        url_profile_request = 'https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%s'
        medias = []
        more_posts_available = True
        max_id = ''
        profile_info = self.get_author_info(usr)
        while more_posts_available:
            variables = {
                'id': str(profile_info.id),
                'first': str(12),
                'after': str(max_id)
            }

            time.sleep(min(random.expovariate(0.6), 15.0))
            response = requests.get(
                url_profile_request % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))),
                headers=headers)

            if not 200 == response.status_code:
                raise print("Your request wasn't send! The status code is: {}".format(response.status_code))

            arr = json.loads(response.text)
            try:
                nodes = arr['data']['user']['edge_owner_to_timeline_media'][
                    'edges']
            except KeyError:
                return {}

            for media in nodes:
                medias.append(media['node'])

            # if there aren't posts in a profile
            if not nodes or nodes == '':
                raise 'NO POSTS IN THIS PROFILE OR IT IS A PRIVATE ACCOUNT!'

            max_id = \
                arr['data']['user']['edge_owner_to_timeline_media'][
                    'page_info'][
                    'end_cursor']
            more_posts_available = \
                arr['data']['user']['edge_owner_to_timeline_media'][
                    'page_info'][
                    'has_next_page']
        return medias

    @staticmethod
    def get_hashtag_post(hashtag: str, headers: dict):
        url_tag_request = 'https://www.instagram.com/graphql/query/?query_id=17875800862117404&variables=%s'
        medias = []
        actual_iteration = 0
        max_iterations = 10
        max_id = ''
        more_posts_available = True
        while actual_iteration <= max_iterations and more_posts_available:
            variables = {
                'tag_name': str(hashtag),
                'first': str(12),
                'after': str(max_id)
            }
            time.sleep(min(random.expovariate(0.6), 15.0))
            response = requests.get(
                url_tag_request % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))),
                headers=headers)

            if response.status_code != 200:
                raise print("Your request wasn't send! The status code is: {}".format(response.status_code))

            arr = response.json()
            try:
                arr['data']['hashtag']['edge_hashtag_to_media']['count']
            except KeyError:
                return []

            nodes = arr['data']['hashtag']['edge_hashtag_to_media']['edges']

            for media in nodes:
                medias.append(media['node'])

            if len(nodes) == 0:
                raise 'NO POSTS WITH THIS HASHTAG!'

            max_id = \
                arr['data']['hashtag']['edge_hashtag_to_media']['page_info'][
                    'end_cursor']
            more_posts_available = \
                arr['data']['hashtag']['edge_hashtag_to_media']['page_info'][
                    'has_next_page']
            actual_iteration += 1

        return medias

    @staticmethod
    def get_comment_answer(id_comment: int, headers: dict):
        url_sub_comment_request = 'https://www.instagram.com/graphql/query/?query_hash=1ee91c32fc020d44158a3192eda98247&variables=%s'
        ans_comment_list = []
        actual_iteration = 0
        max_iterations = 10
        max_id = ''
        more_posts_available = True
        while actual_iteration <= max_iterations and more_posts_available:
            variables = {
                'comment_id': str(id_comment),
                'first': str(12),
                'after': str(max_id)
            }
            time.sleep(min(random.expovariate(0.6), 15.0))
            response = requests.get(
                url_sub_comment_request % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))),
                headers=headers)
            if response.status_code != 200:
                raise print("Your request wasn't send! The status code is: {}".format(response.status_code))

            arr = response.json()
            nodes = arr['data']['comment']['edge_threaded_comments']['edges']

            if len(nodes) != 0:
                for media in nodes:
                    ans_comment_list.append(media['node'])

            max_id = \
                arr['data']['comment']['edge_threaded_comments']['page_info'][
                    'end_cursor']
            more_posts_available = \
                arr['data']['comment']['edge_threaded_comments']['page_info'][
                    'has_next_page']
            actual_iteration += 1

        return ans_comment_list

    @staticmethod
    def get_comments(shortcode: str, headers: dict):
        url_comments_request = 'https://www.instagram.com/graphql/query/?query_id=17852405266163336&variables=%s'
        comment_list = []
        actual_iteration = 0
        max_iterations = 10
        max_id = ''
        more_posts_available = True
        while actual_iteration <= max_iterations and more_posts_available:
            variables = {
                'shortcode': str(shortcode),
                'first': str(12),
                'after': str(max_id)
            }
            time.sleep(min(random.expovariate(0.6), 15.0))
            response = requests.get(
                url_comments_request % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':'))),
                headers=headers)
            if response.status_code != 200:
                raise print("Your request wasn't send! The status code is: {}".format(response.status_code))

            arr = response.json()
            nodes = arr['data']['shortcode_media']['edge_media_to_comment']['edges']

            if len(nodes) != 0:
                for media in nodes:
                    comment_list.append(media['node'])

            max_id = \
                arr['data']['shortcode_media']['edge_media_to_comment']['page_info'][
                    'end_cursor']
            more_posts_available = \
                arr['data']['shortcode_media']['edge_media_to_comment']['page_info'][
                    'has_next_page']
            actual_iteration += 1

        return comment_list

    def get_post_info(self, actual_post: dict, headers: dict):
        url_post_request = 'https://www.instagram.com/p/' + actual_post['shortcode'] + '/?__a=1'
        time.sleep(min(random.expovariate(0.6), 15.0))
        response = requests.get(url_post_request, headers=headers)
        if response.status_code != 200:
            raise print("Your request wasn't send! The status code is: {}".format(response.status_code))
        arr = response.json()
        try:
            arr['items']
        except KeyError:
            return []
        post_info = arr['items'][0]

        # AUTHOR OF POST INFO
        author_info = self.get_author_info(post_info['user']['username'])

        # MEDIA
        if 'carousel_media' in post_info:
            post_media = []
            for n in post_info['carousel_media']:
                if n['media_type'] == 2:
                    post_media.append(n['video_versions'][0]['url'])
                else:
                    post_media.append(n['image_versions2']['candidates'][0]['url'])
        elif post_info['media_type'] == 1:
            post_media = post_info['image_versions2']['candidates'][0]['url']
        else:
            post_media = post_info['video_versions'][0]['url']

        # COMMENTS
        f_comments = []
        comments = self.get_comments(actual_post['shortcode'], headers)
        if len(comments) != 0:
            for cmt in comments:
                id_f_comment = [comm.id for comm in f_comments]
                if cmt['id'] not in id_f_comment:
                    cmt_author_info = self.get_author_info(cmt['owner']['username'])
                    f_comments.append(comment.Comment(cmt['id'], cmt_author_info, cmt['text']))
                    ans_comments = self.get_comment_answer(cmt['id'], headers)
                    if len(ans_comments) != 0:
                        for ans_cmt in ans_comments:
                            ans_cmt_author_info = self.get_author_info(ans_cmt['owner']['username'])
                            f_comments.append(comment.Comment(ans_cmt['id'], ans_cmt_author_info, ans_cmt['text'], True,
                                                              cmt['id']))

        else:
            f_comments.append('Nessun commento in questo post!')

        return post.Post(actual_post['shortcode'],
                         author_info,
                         actual_post['edge_media_to_caption']['edges'][0]['node']['text'],
                         post_media,
                         reaction.Reaction(post_info['like_count'],
                                           f_comments,
                                           post_info['comment_count']))

    # METODO UTILIZZATO CON IL PACCHETTO INSTASCRAPE, QUINDI MOMENTANEAMENTE MESSO DA PARTE...
    def post_results(self, post_info: dict, author_info: author.Author):
        post_text = (post_info['edge_media_to_caption']['edges'][0]['node']['text']
                     if len(post_info['edge_media_to_caption']['edges']) != 0
                     else 'Nessuna descrizione!')
        if post_info['__typename'] == "GraphSidecar":
            post_media = []
            nodes = [e['node'] for e in post_info['edge_sidecar_to_children']['edges']]
            for n in nodes:
                if n['is_video']:
                    post_media.append(n['video_url'])
                else:
                    post_media.append(n['display_url'])
        elif post_info['is_video']:
            post_media = post_info['video_url']
        else:
            post_media = post_info['display_url']

        comment_list = []
        if post_info['edge_media_to_parent_comment']['count'] != 0:
            comments = [cmt['node'] for cmt in post_info['edge_media_to_parent_comment']['edges']]
            for cmt in comments:
                cmt_author_info = self.get_author_info(cmt['owner']['username'])
                comment_list.append(comment.Comment(cmt['id'], cmt_author_info, cmt['text']))
                if cmt['edge_threaded_comments']['count'] != 0:
                    answer_comments = [ans_cmt['node'] for ans_cmt in cmt['edge_threaded_comments']['edges']]
                    for ans_cmt in answer_comments:
                        ans_cmt_author_info = self.get_author_info(ans_cmt['owner']['username'])
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
        self.logger = logging.getLogger('SOCMINT.InstascrapeBaseService')
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
