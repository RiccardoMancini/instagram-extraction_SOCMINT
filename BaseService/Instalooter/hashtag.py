from instalooter.looters import HashtagLooter
from BaseService.Instalooter.instalooter_scraper import InstalooterScraper
from datetime import datetime


class Hashtag(InstalooterScraper):
    """
    This class defines the hashtag structure using Instalooter
    """

    def __init__(self, username: str, password: str, hashtag: str,
                 since: datetime = None, until: datetime = None):
        """
        To init the object the information about
        :param hashtag: the hashtag of Instagram to scrape
        :param since: time limit from which to scrape data
        :param until: time limit not to be exceeded to scrape data
        """
        super().__init__(username, password)
        self.hashtag = hashtag
        self.since = since if since is not None else datetime.min
        self.until = until if until is not None else datetime.now()

    def get_posts_by_hashtag(self):
        scraped_posts = []
        i = 0
        posts_limit = 5
        medias = []
        looter = HashtagLooter(self.hashtag)
        session = self.check_log(looter)

        for item in looter.medias():
            if i < posts_limit:
                medias.append(item)
                i += 1
            else:
                break

        for media in medias:
            post_info = looter.get_post_info(media['shortcode'])
            date = datetime.fromtimestamp(post_info['taken_at_timestamp'])
            if self.until > date >= self.since:
                scraped_posts.append(self.post_results(post_info, session))
        return scraped_posts
