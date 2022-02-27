import praw
from praw.models import InlineImage
import feedparser
import json

CLIENT_ID = 'pm25UeetuPduMhmHDgfocQ'
SECRET_KEY = '-kHk4dAxWCAkfrbpM1Mz8EZ1qlZRBw'

#open json confif file if possible
try:
    f = open('config.json') #file opened for reading
    data = json.load(f)
    f.close()
except:
    print('Error opening config file.  Ensure config.json is present in same directory as bot.py')
    exit()

reddit = praw.Reddit(
    client_id=data['client_id'],
    client_secret=data['client_secret_key'],
    user_agent=data['user_agent'],
    username=data['username'],
    password=data['password']
)

#this supresses praw warnings
reddit.validate_on_submit = True

RSSfeed = feedparser.parse(data['rss_feed'])
newestEpisode = RSSfeed.entries[0] #this will always be the most recent entry in the feed

# the next 4 lines take away the html tags (will eventually be changed to anything between <>)
neatSummaryText = newestEpisode.summary
neatSummaryText = neatSummaryText.replace('<p>', '')
neatSummaryText = neatSummaryText.replace('</p>', '')
neatSummaryText = neatSummaryText.replace('<br />', '')

media = {}
selftext = ''
#check to see if an image is included
if (data['image_filename'] != ""):
    image = InlineImage(data['image_filename'], data['image_caption'])
    selftext = '{image1}'
    media = {"image1": image}

#this loop adds all platforms from config file and uses markdown to make them look nice
selftext += neatSummaryText + '\n\n# Find us here: \n\n'
for platform in data['platforms']:
    selftext += '### [' + platform['name'] + '](' + platform['link'] + ')\n\n'

#this is where the magic happens
for sub in data['subreddits']:
    reddit.subreddit(sub).submit(newestEpisode.title, selftext=selftext, inline_media=media)
