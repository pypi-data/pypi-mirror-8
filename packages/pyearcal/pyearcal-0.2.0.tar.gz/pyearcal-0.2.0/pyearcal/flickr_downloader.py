import urllib2
import random
import os
from image_sources import SortedImageDirectory
from BeautifulSoup import BeautifulStoneSoup

TEMP_DIR = '.flickr-download'
EXTENSION = '.jpg'

class FlickrDownloader(SortedImageDirectory):
    '''Image source that downloads random pictures from Flickr.

    Based on the article
        http://blog.art21.org/2011/09/20/how-to-use-python-to-create-a-simple-flickr-photo-glitcher
    '''
    def download_images(self, number=12):
        response = urllib2.urlopen('http://api.flickr.com/services/feeds/photos_public.gne?tags=' + self.keyword + '&lang=en-us&format=rss_200')
        soup = BeautifulStoneSoup(response)
     
        image_list = []
        for image in soup.findAll('media:content'):
            image_url = dict(image.attrs)['url']
            image_list.append(image_url)
        image_list = random.sample(image_list, number)
     
        if not os.path.isdir(TEMP_DIR):
            os.makedirs(TEMP_DIR)
        for index, image in enumerate(image_list):
            response = urllib2.urlopen(image)
            with open(os.path.join(TEMP_DIR, '%d%s' % (index+1, EXTENSION)), 'wb') as output_file:
                output_file.write(response.read())
            response.close()
            print 'Downloaded picture %d of %d from flickr.' % (index+1, number)

    def __init__(self, keyword='python'):
        '''        
        :param keyword: a keyword to look for on flickr.
        '''
        self.keyword = keyword
        self.dirname = TEMP_DIR
        self.extension = EXTENSION
        self.download_images()
        self.read_images()