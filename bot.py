import praw #this lets us talk to the reddit API
from praw.models import InlineImage #easiest way to add image to our post
import feedparser #allows us to get rss feed data
import json #allows us to put json configuration data into a dictionary
import sys #lets us get command line arguments
from datetime import datetime # lets us run the script every week but only post if a new episode is added to the rss feed

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

#check the time that the last episode was added to the rss feed
timeTuple = newestEpisode.published_parsed
currentTime = datetime.now().timetuple()

if (timeTuple.tm_yday >= currentTime.tm_yday - 7 or timeTuple.tm_year > currentTime.tm_year):
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

    #if statement allows you to add a testing flag so the bot doesnt actually try to post on reddit
    if (len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != 't')):
        #this is where the magic happens
        for sub in data['subreddits']:
            reddit.subreddit(sub).submit(newestEpisode.title, selftext=selftext, inline_media=media)





