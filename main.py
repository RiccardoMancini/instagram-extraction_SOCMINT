from datetime import datetime
from BaseService.Instaloader.profile import Profile as ProfInstaloader
from BaseService.Instaloader.hashtag import Hashtag as HashInstaloader
from BaseService.Instalooter.profile import Profile as ProfInstalooter
from BaseService.Instalooter.hashtag import Hashtag as HashInstalooter
from BaseService.Hm_instascrape.profile import Profile as ProfInstascrape
from BaseService.Hm_instascrape.hashtag import Hashtag as HashInstascrape

"""
Credenziali login
"""
USERNAME = 'uni_scraper'
PASSWORD = 'Scraper2021'

"""
TEST INSTALOADER
"""
#new = ProfInstaloader(USERNAME, PASSWORD, '_martinapaoletti')
#posts = new.get_posts_by_profile()
#new = HashInstaloader(USERNAME, PASSWORD, 'python')
#posts = new.get_posts_by_hashtag()

"""
TEST INSTALOOTER //Abbandonato al suo destino....
"""
#new2 = ProfInstalooter(USERNAME, PASSWORD, '_martinapaoletti')
#posts = new2.get_posts_by_profile()
#new2 = HashInstalooter(USERNAME, PASSWORD, 'python')
#posts = new2.get_posts_by_hashtag()

"""
TEST INSTASCRAPE
"""
new3 = ProfInstascrape(USERNAME, PASSWORD, '_martinapaoletti')
posts = new3.get_posts_by_profile()
#new3 = HashInstascrape(USERNAME, PASSWORD, 'python')
#posts = new3.get_posts_by_hashtag()


"""
PRINT DEI DATI ESTRATTI
"""
for post in posts:
    print('\nShortcode:', post.id,
          '\nDescrizione:', post.text,
          '\nAutore del post:', [post.author.id, post.author.username, post.author.name, post.author.follower,
                                 post.author.following, post.author.n_posts, post.author.platform],
          '\nNumero di like:', post.reaction.like_count,
          '\nNumero di commenti', post.reaction.n_comment,
          '\nURL media:', post.media_url,
          '\nCommenti:', [x if type(x) is str else [x.id, x.author.username, x.text, x.answer, x.id_comment] for x in post.reaction.comments])

"""TEST INSTAGRAPI"""

#from instagrapi import Client

#cl = Client()
#cl.login(USERNAME, PASSWORD)

#user_id = cl.user_id_from_username("_martinapaoletti")
#medias = cl.user_medias(user_id)

#print(len(medias))

#hashtag = cl.hashtag_info_a1('italia')
#print(hashtag.media_count)
#cl.logout()

"""TEST"""
"""from instascrape import *

google_post = Post('CYMQ5lCsKpkOM2rzp5UQNcw9DCfztqnCWlh5lc0')


google_post.scrape(headers="{'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57', "
                           "'cookie': 'sessionid=48731031385%3A2UNLWtiAd34kep%3A5;")


print(google_post['hashtags'])"""
