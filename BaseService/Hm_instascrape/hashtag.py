#from instascrape.scrapers import Hashtag as Hashtag_instascrape, Post as Post_instascrape
from BaseService.Hm_instascrape.hm_instascrape_scraper import HmInstaScrapeScraper


class Hashtag(HmInstaScrapeScraper):
    def __init__(self, username: str, password: str, hashtag: str):
        super().__init__(username, password)
        self.hashtag = hashtag

    def get_posts_by_hashtag(self):
        scraped_posts = []
        session_utils = self.get_insta_session()
        headers = {
            "user-agent": self.user_agent,
            "cookie": f"sessionid={session_utils['session_id']};"
        }
        posts = self.get_hashtag_post(self.hashtag, headers)
        for post in posts[:5]:
            scraped_posts.append(self.get_post_info(post, headers))

            """OLD VERSION USING INSTASCRAPE...
            post_obj = Post_instascrape(post['shortcode'])
            post_obj.scrape(headers=headers)
            post_info = post_obj.json_dict["graphql"]["shortcode_media"]
            author_username = post_obj.json_dict["graphql"]["shortcode_media"]['owner']['username']
            author_info = self.get_author_info(author_username)
            scraped_posts.append(self.post_results(post_info, author_info))"""

        return scraped_posts
