#########################################
####nCore CouchPotato TorrentProvider####
############# @by gala ##################
############### 2015 ####################
#########################################
from couchpotato.core.logger import CPLog
from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
import traceback
import simplejson

log = CPLog(__name__)

class nCore(TorrentProvider, MovieProvider):
    urls = {
        'login': 'https://ncore.cc/login.php',
        'search': 'https://ncore.cc/torrents.php?mire=%s&miben=name&tipus=all&submit=Ok&searchedfrompotato=true&jsons=true&tags=',
    }

    http_time_between_calls = 1  # seconds

    def _searchOnTitle(self, title, movie, quality, results):
        url = self.urls['search'] % (tryUrlencode(title))
        data = simplejson.loads(simplejson.dumps(self.getJsonData(url)))
        #data=json.loads(data)
        if data:
            try:
                for d in data['results']:
                    log.info('Number of torrents found on nCore = ' + str(data['total_results']))
                    results.append({
                        'id': d['torrent_id'],
                        'leechers': d['leechers'],
                        'seeders': d['seeders'],
                        'name': d['release_name'],
                        'url': d['download_url'],
                        'detail_url': ['details_url'],
                        'size': self.parseSize(d['size']),
                    })
            except:
                log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))

    def getLoginParams(self):
        return {
            'nev': str(self.conf('username')),
            'pass': str(self.conf('password')),
            'submitted': 1
        }

    def successLogin(self, output):
       return 'exit.php' in output.lower()

    loginCheckSuccess = successLogin