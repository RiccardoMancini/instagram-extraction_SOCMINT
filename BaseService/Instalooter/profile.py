from instalooter._utils import get_shared_data
from instalooter.looters import ProfileLooter
from BaseService.Instalooter.instalooter_scraper import InstalooterScraper
from datetime import datetime


class Profile(InstalooterScraper):
    """
       This class defines the profile structure using Instalooter
       """
    def __init__(self, username: str, password: str, usr: str,
                 since: datetime = None, until: datetime = None):
        """
        To init the object the information about
        :param usr: the username of Instagram profile to scrape
        :param since: time limit from which to scrape data
        :param until: time limit not to be exceeded to scrape data
        """
        super().__init__(username, password)
        self.usr = usr
        self.since = since if since is not None else datetime.min
        self.until = until if until is not None else datetime.now()

    def get_posts_by_profile(self):
        scraped_posts = []
        looter = ProfileLooter(self.usr)
        session = self.check_log(looter)
        medias = list(looter.medias())
        for media in medias[:5]:
            post_info = looter.get_post_info(media['shortcode'])
            date = datetime.fromtimestamp(post_info['taken_at_timestamp'])
            if self.until > date >= self.since:
                scraped_posts.append(self.post_results(post_info, session))
        return scraped_posts
