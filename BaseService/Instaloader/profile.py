import instaloader
from instaloader import Profile as Instaloader_profile, Post
from BaseService.Instaloader.instaloader_scraper import InstaloaderScraper


class Profile(InstaloaderScraper):
    """
    This class defines the profile structure using Instaloader
    """

    def __init__(self, username: str, password: str, usr: str):
        """
        To init the object the information about
        :param usr: the username of Instagram profile to scrape
        """
        super().__init__(username, password)
        self.usr = usr

    def get_posts_by_profile(self):
        scraped_posts = []
        self.check_log()
        posts_node = Instaloader_profile.from_username(self.ist.context, self.usr).get_posts()
        posts = list(posts_node)
        for post in posts[:10]:
            if self.until > post.date >= self.since:
                scraped_posts.append(self.post_results(post))
        return scraped_posts
