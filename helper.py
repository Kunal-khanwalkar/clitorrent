import requests
import os

class TorrentAPI():
    #Initialize Headers
    def __init__(self):    
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    #Receiving Site Response
    def fetchSite(self, url):
        print('Fetching site...')
        try:
            result = requests.get(url, headers=self.headers) 
            result.raise_for_status()
            return result
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

    #Webtorrent Download
    def download_torrent(self,magnet):
        os.system('aria2c ' + f'\"{magnet}\"')

if __name__=='__main__':
    API = TorrentAPI()
    magnet = input('Enter magnet link: ')
    API.download_torrent(magnet)
