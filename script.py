from lxml import html
from helper import TorrentAPI

API = TorrentAPI()
SITE_GOG = 'https://freegogpcgames.com/'
SITE_1337 = 'https://1337x.wtf'

def get_gog(Search_query):
    Search_query = Search_query.replace(' ','+')
    url = f'{SITE_GOG}/?s={Search_query}'    
    result = API.fetchSite(url)
    tree = html.fromstring(result.content)
    table_of_contents = tree.xpath('/html/body/div[1]/div/div/main/div/article')[:10]

    if len(table_of_contents) == 0:
        raise SystemExit('No Entries found')

    for idx,item in enumerate(table_of_contents):
        item = item.xpath('./div/header/h2/a')[0]
        print('\n-\n' + str(idx+1) + ').' + item.text_content(),end='')
    print('\n')
    

    option = int(input('Enter option: '))-1
    torrent = table_of_contents[option].xpath('./div/header/h2/a')[0].attrib.get('href')
    
    result = API.fetchSite(torrent)
    tree = html.fromstring(result.content)

    download_link = tree.xpath('/html/body/div[1]/div/div[1]/main/article/div/div[1]/p[7]/strong/a')[0].attrib.get('href')
    result = API.fetchSite(torrent)
    tree = html.fromstring(result.content)

    magnet_link = tree.xpath('//*[@id=""]/div[2]/p[18]/strong/a')[0].attrib.get('href')
    print(f'\"{magnet_link}\"')
    API.download_torrent(magnet_link)

def get_1337(Search_query):
    Search_query = Search_query.replace(' ','+')
    url = f'{SITE_1337}/search/{Search_query}/1/'
    result = API.fetchSite(url)
    tree = html.fromstring(result.content)
    table_of_contents = tree.xpath('/html/body/main/div/div/div/div[2]/div[1]/table/tbody')[0]

    if len(table_of_contents) == 0:
        raise SystemExit('No Entries Found')

    headings = ['Seeders', 'Leechers', 'Date of Upload', 'Size', 'Uploader']

    for idx,row in enumerate(table_of_contents):
        print('\n-\n' + str(idx+1) + '). ' + row[0].text_content())
        for i,col in enumerate(row[1:]):
            print(headings[i] + ' : ' + col.text_content() + ', ',end='')        
    print('\n')

    option = input('Enter option: ')
    torrent = SITE_1337 + table_of_contents.xpath('./tr[' + option + ']/td/a[2]')[0].attrib.get('href')

    result = API.fetchSite(torrent)
    tree = html.fromstring(result.content)

    magnet_link = tree.xpath('/html/body/main/div/div/div/div[2]/div[1]/ul[1]/li[1]/a')[0].attrib.get('href')    
    print(f'\"{magnet_link}\"')
    API.download_torrent(magnet_link)

def main():
    Search_query = input('Search Query: ')
    Site = int(input('Available platforms:\n1. GOG\n2. 1337\nChoose platform: '))
    match Site:
        case 1:
            get_gog(Search_query)
        case 2:
            get_1337(Search_query)        
    raise SystemExit('Invalid Choice')

if __name__=='__main__':
    main()
