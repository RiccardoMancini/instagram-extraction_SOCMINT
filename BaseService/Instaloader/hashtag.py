from instaloader import NodeIterator, Post
from BaseService.Instaloader.instaloader_scraper import InstaloaderScraper


class Hashtag(InstaloaderScraper):
    """
    This class defines the hashtag structure using Instaloader
    """
    def __init__(self, username: str, password: str, hashtag: str):
        """
        To init the object the information about
        :param hashtag: the hashtag of Instagram to scrape
        """
        super().__init__(username, password)
        self.hashtag = hashtag

    def get_posts_by_hashtag(self):
        scraped_posts = []
        i = 0
        posts_limit = 5
        posts = []
        self.check_log()
        posts_iterator = NodeIterator(
            self.ist.context, "9b498c08113f1e09617a1703c22b2f32",
            lambda d: d['data']['hashtag']['edge_hashtag_to_media'],
            lambda n: Post(self.ist.context, n),
            {'tag_name': self.hashtag},
            f"https://www.instagram.com/explore/tags/{self.hashtag}/"
        )
        for item in posts_iterator:
            if i < posts_limit:
                posts.append(item)
                i += 1
            else:
                break

        for post in posts:
            if self.until > post.date >= self.since:
                scraped_posts.append(self.post_results(Post.from_shortcode(self.ist.context, post.shortcode)))
        return scraped_posts
