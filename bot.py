import praw
from praw.models import InlineImage
import feedparser
import json

CLIENT_ID = 'pm25UeetuPduMhmHDgfocQ'
SECRET_KEY = '-kHk4dAxWCAkfrbpM1Mz8EZ1qlZRBw'

#open json confif file
f = open('config.json')
data = json.load(f)

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


#put together the contents of the post
selftext += neatSummaryText \
+ '\n\n# Find us here: \n\n' \
+ '### **Anchor.fm:** https://anchor.fm/manswithopinions/episodes/Mans-With-Opinions-V2-3-e1e11lj \n\n' \
+ '### **Spotify:** https://open.spotify.com/show/2QttwoLNUprOBZaazsJJ7U \n\n' \
+ '### **Google Podcasts:** https://podcasts.google.com/feed/aHR0cHM6Ly9hbmNob3IuZm0vcy84MjQxNWU3NC9wb2RjYXN0L3Jzcw \n\n' \
+ '### **Apple Podcasts:** https://podcasts.apple.com/us/podcast/mans-with-opinions/id1608806064 \n\n' \
+ '### **Youtube:** https://www.youtube.com/watch?v=MB0f4uR-yZ4&t=16s \n\n'

#this is where the magic happens
for sub in data['subreddits']:
    reddit.subreddit(sub).submit(newestEpisode.title, selftext=selftext, inline_media=media)
